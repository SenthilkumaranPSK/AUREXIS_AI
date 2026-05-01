"""
Database utility functions for AUREXIS AI
"""

import sqlite3
import aiosqlite
from contextlib import asynccontextmanager, contextmanager
from typing import Generator, AsyncGenerator, Optional, Dict, Any
import logging
import threading
from queue import Queue, Empty
import time
from dataclasses import dataclass

from config_enhanced import settings
from exceptions import DatabaseError

logger = logging.getLogger(__name__)


# Functions related to connection pooling and management
# These are now centralized here to manage the pool and provide access via get_db/get_async_db

@dataclass
class ConnectionPoolConfig:
    """Database connection pool configuration"""
    min_connections: int = 2
    max_connections: int = 10
    max_idle_time: int = 300  # 5 minutes
    connection_timeout: int = 30
    check_interval: int = 60  # 1 minute


class DatabaseConnectionPool:
    """Thread-safe database connection pool"""
    
    def __init__(self, database_path: str, config: ConnectionPoolConfig):
        self.database_path = database_path
        self.config = config
        self.pool = Queue(maxsize=config.max_connections)
        self.active_connections = 0
        self.lock = threading.Lock()
        self.last_check = time.time()
        
        # Initialize minimum connections
        self._initialize_pool()
        
        # Start maintenance thread
        self._start_maintenance_thread()
    
    def _initialize_pool(self):
        """Initialize the pool with minimum connections"""
        for _ in range(self.config.min_connections):
            conn = self._create_connection()
            if conn:
                self.pool.put(conn)
                self.active_connections += 1
    
    def _create_connection(self) -> Optional[sqlite3.Connection]:
        """Create a new database connection with security settings"""
        try:
            conn = sqlite3.connect(
                self.database_path,
                check_same_thread=False,
                timeout=self.config.connection_timeout
            )
            conn.row_factory = sqlite3.Row
            
            # Security settings
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.execute("PRAGMA cache_size = 10000")
            conn.execute("PRAGMA temp_store = MEMORY")
            
            return conn
        except Exception as e:
            logger.error(f"Error creating database connection: {e}")
            return None
    
    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Get a connection from the pool"""
        conn = None
        try:
            # Try to get connection from pool
            try:
                conn = self.pool.get(timeout=self.config.connection_timeout)
            except Empty:
                # Create new connection if pool is empty and under max limit
                with self.lock:
                    if self.active_connections < self.config.max_connections:
                        conn = self._create_connection()
                        if conn:
                            self.active_connections += 1
                    else:
                        # Wait for available connection
                        conn = self.pool.get(timeout=self.config.connection_timeout)
            
            if not conn:
                raise DatabaseError("Failed to acquire database connection")
            
            # Check if connection is still valid
            if not self._is_connection_valid(conn):
                conn.close()
                conn = self._create_connection()
                if not conn:
                    raise DatabaseError("Failed to create valid database connection")
            
            yield conn
            
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise DatabaseError(f"Database operation failed: {e}")
        finally:
            if conn:
                try:
                    # Return connection to pool
                    self.pool.put(conn, timeout=1)
                except:
                    # Pool is full, close connection
                    conn.close()
                    with self.lock:
                        self.active_connections -= 1
    
    def _is_connection_valid(self, conn: sqlite3.Connection) -> bool:
        """Check if connection is still valid"""
        try:
            conn.execute("SELECT 1")
            return True
        except:
            return False
    
    def _start_maintenance_thread(self):
        """Start maintenance thread for connection pool"""
        def maintenance():
            while True:
                time.sleep(self.config.check_interval)
                self._maintain_pool()
        
        thread = threading.Thread(target=maintenance, daemon=True)
        thread.start()
    
    def _maintain_pool(self):
        """Maintain connection pool - remove idle connections"""
        current_time = time.time()
        if current_time - self.last_check < self.config.check_interval:
            return
        
        # This is a simplified maintenance - in production, you'd want
        # more sophisticated connection health checking
        self.last_check = current_time
    
    def close_all(self):
        """Close all connections in the pool"""
        while not self.pool.empty():
            try:
                conn = self.pool.get_nowait()
                conn.close()
                self.active_connections -= 1
            except Empty:
                break


# Global connection pool instance and context manager
_connection_pool: Optional[DatabaseConnectionPool] = None

# Functions to manage the connection pool and get connections
# get_db and get_async_db are defined directly in this module to avoid circular imports.
# connection_enhanced.py depends on these utilities.

def get_connection_pool() -> DatabaseConnectionPool:
    """Get or create the global connection pool"""
    global _connection_pool
    
    if _connection_pool is None:
        database_path = settings.DATABASE_URL.replace("sqlite:///", "")
        config = ConnectionPoolConfig(
            min_connections=2,
            max_connections=settings.DATABASE_POOL_SIZE,
            connection_timeout=settings.DATABASE_POOL_TIMEOUT
        )
        _connection_pool = DatabaseConnectionPool(database_path, config)
    
    return _connection_pool

@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Get database connection from the pool"""
    # Corrected: Removed self-import 'from database.db_utils import get_db'.
    # get_db is defined within this module and should be directly accessible.
    pool = get_connection_pool()
    with pool.get_connection() as conn:
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

@asynccontextmanager
async def get_async_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    """Async database context manager"""
    database_path = settings.DATABASE_URL.replace("sqlite:///", "")
    
    conn = None
    try:
        conn = await aiosqlite.connect(
            database_path,
            check_same_thread=False
        )
        
        # Enable WAL mode for better concurrency
        await conn.execute("PRAGMA foreign_keys = ON")
        await conn.execute("PRAGMA journal_mode = WAL")
        await conn.execute("PRAGMA cache_size = 10000")
        await conn.execute("PRAGMA temp_store = MEMORY")
        
        yield conn
        
        await conn.commit()
    except Exception as e:
        if conn:
            await conn.rollback()
        raise DatabaseError(f"Async database operation failed: {e}")
    finally:
        if conn:
            await conn.close()


def init_database():
    """Enhanced database initialization with indexes and constraints"""
    try:
        # Ensure pool is reset and any existing connections are closed
        close_connection_pool()
        global _connection_pool
        _connection_pool = None # Reset the global pool reference

        with get_db() as conn: # conn is obtained here
            cursor = conn.cursor()
            
            # Create tables with proper constraints
            _create_users_table(cursor)
            _create_financial_tables(cursor)
            _create_chat_tables(cursor)
            _create_system_tables(cursor)
            
            # Create indexes for performance
            _create_indexes(cursor)
            
            # Insert sample data if needed
            _insert_sample_data(conn) # Pass the obtained conn object
            
            conn.commit()
            logger.info("Enhanced database initialized successfully")
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise DatabaseError("Database initialization failed")


def _create_users_table(cursor: sqlite3.Cursor):
    """Create users table with proper constraints"""
    # Only create table if it doesn't exist (don't drop existing data)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL CHECK(length(name) >= 2),
            email TEXT UNIQUE NOT NULL CHECK(email LIKE '%@%.%'),
            password_hash TEXT NOT NULL CHECK(length(password_hash) > 0),
            user_number TEXT UNIQUE NOT NULL CHECK(length(user_number) >= 8),
            occupation TEXT CHECK(length(occupation) >= 2),
            age INTEGER CHECK(age >= 18 AND age <= 120),
            location TEXT CHECK(length(location) >= 2),
            is_active BOOLEAN DEFAULT 1 CHECK(is_active IN (0, 1)),
            is_verified BOOLEAN DEFAULT 0 CHECK(is_verified IN (0, 1)),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            login_attempts INTEGER DEFAULT 0 CHECK(login_attempts >= 0),
            locked_until TIMESTAMP
        )
    """)


def _create_financial_tables(cursor: sqlite3.Cursor):
    """Create financial data tables"""
    # Monthly income table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monthly_income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            month DATE NOT NULL CHECK(month IS date(month, '+0 days')),
            amount REAL NOT NULL CHECK(amount > 0),
            source TEXT CHECK(length(source) >= 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(user_id, month)
        )
    """)
    # Expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            date DATE NOT NULL CHECK(date IS date(date, '+0 days')),
            amount REAL NOT NULL CHECK(amount > 0),
            category TEXT NOT NULL CHECK(length(category) >= 2),
            description TEXT CHECK(length(description) >= 2),
            merchant TEXT CHECK(length(merchant) >= 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    # Goals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL CHECK(length(name) >= 2),
            target_amount REAL NOT NULL CHECK(target_amount > 0),
            current_amount REAL DEFAULT 0 CHECK(current_amount >= 0),
            deadline DATE CHECK(deadline IS date(deadline, '+0 days') OR deadline IS NULL),
            category TEXT CHECK(length(category) >= 2),
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'completed', 'paused')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)


def _create_chat_tables(cursor: sqlite3.Cursor):
    """Create chat-related tables"""
    # Chat sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id TEXT PRIMARY KEY CHECK(length(id) >= 10),
            user_id TEXT NOT NULL,
            title TEXT CHECK(length(title) >= 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    # Chat messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
            content TEXT NOT NULL CHECK(length(content) >= 1),
            metadata TEXT,  -- JSON metadata
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
        )
    """)


def _create_system_tables(cursor: sqlite3.Cursor):
    """Create system tables"""
    # Alerts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            type TEXT NOT NULL CHECK(length(type) >= 2),
            title TEXT NOT NULL CHECK(length(title) >= 2),
            message TEXT NOT NULL CHECK(length(message) >= 2),
            severity TEXT NOT NULL CHECK(severity IN ('low', 'medium', 'high', 'critical')),
            is_read BOOLEAN DEFAULT 0 CHECK(is_read IN (0, 1)),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    # Audit log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            action TEXT NOT NULL CHECK(length(action) >= 2),
            resource TEXT,
            details TEXT,  -- JSON details
            ip_address TEXT,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        )
    """)


def _create_indexes(cursor: sqlite3.Cursor):
    """Create performance indexes"""
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
        "CREATE INDEX IF NOT EXISTS idx_users_user_number ON users(user_number)",
        "CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active)",
        "CREATE INDEX IF NOT EXISTS idx_expenses_user_date ON expenses(user_id, date)",
        "CREATE INDEX IF NOT EXISTS idx_expenses_user_category ON expenses(user_id, category)",
        "CREATE INDEX IF NOT EXISTS idx_income_user_month ON monthly_income(user_id, month)",
        "CREATE INDEX IF NOT EXISTS idx_goals_user_status ON goals(user_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_chat_messages_session_created ON chat_messages(session_id, created_at)",
        "CREATE INDEX IF NOT EXISTS idx_alerts_user_read ON alerts(user_id, is_read)",
        "CREATE INDEX IF NOT EXISTS idx_audit_user_created ON audit_log(user_id, created_at)",
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)
    
    logger.info("Database indexes created successfully")


def _insert_sample_data(conn: sqlite3.Connection): # Accept conn parameter
    """Insert sample data if tables are empty"""
    cursor = conn.cursor() # Create cursor from conn
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if user_count == 0:
        # Import and create sample users
        # Use UserManager directly to ensure hashing and user_number generation
        sample_users_data = [
            {"id": "user_1", "user_number": "88888888", "name": "Imayavarman", "email": "imayavarman@aurexis.ai", "password": "Imayavarman@2000", "occupation": "Software Engineer", "age": 28, "location": "Chennai"},
            {"id": "user_2", "user_number": "77777777", "name": "Thiruvalluvar", "email": "thiruvalluvar@aurexis.ai", "password": "Thiruvalluvar@2000", "occupation": "Philosopher", "age": 35, "location": "Madurai"},
            {"id": "user_3", "user_number": "66666666", "name": "PonniyinSelvan", "email": "ponniyinselvan@aurexis.123", "password": "PonniyinSelvan@2000", "occupation": "Royal Consultant", "age": 30, "location": "Thanjavur"},
            {"id": "user_4", "user_number": "55555555", "name": "Karkal", "email": "karkal@aurexis.ai", "password": "Karkal@2000", "occupation": "Architecture Designer", "age": 32, "location": "Kanchi"},
            {"id": "user_5", "user_number": "44444444", "name": "Senthil", "email": "senthil@aurexis.ai", "password": "Senthil@2000", "occupation": "Data Scientist", "age": 26, "location": "Coimbatore"},
        ]
        
        for user_data in sample_users_data:
            try:
                # Import UserManager locally to resolve potential circular import
                from user_manager_secure import UserManager
                UserManager.create_user(user_data, conn) # Pass conn here
            except Exception as e:
                logger.warning(f"Skipping user creation for {user_data.get('email')}: {e}")
        
        logger.info(f"Initialized {len(sample_users_data)} sample users")

def close_connection_pool():
    """Close the global connection pool"""
    global _connection_pool
    if _connection_pool:
        _connection_pool.close_all()
        _connection_pool = None


if __name__ == "__main__":
    init_database()
