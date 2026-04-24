"""
AUREXIS AI — Database Layer
SQLAlchemy models and database session management
"""

from sqlalchemy import create_engine, Column, String, Integer, Float, JSON, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
from datetime import datetime, timezone
from typing import Generator
from contextlib import contextmanager

from config import settings


# ── Database Setup ─────────────────────────────────────────────────────────

# Use StaticPool for SQLite to avoid threading issues
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ── Database Models ────────────────────────────────────────────────────────

class User(Base):
    """User model with authentication and profile data"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)  # user_number
    name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    
    # Profile
    occupation = Column(String)
    age = Column(Integer)
    location = Column(String)
    
    # Banking
    account_number = Column(String)
    bank_name = Column(String)
    account_type = Column(String)
    bank_location = Column(String)
    credit_card = Column(Boolean, default=False)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    chat_history = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"


class ChatHistory(Base):
    """Chat conversation history"""
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), index=True)
    
    # Metadata
    model = Column(String)  # Ollama model used
    tokens = Column(Integer)  # Token count
    duration_ms = Column(Float)  # Response time
    
    # Relationships
    user = relationship("User", back_populates="chat_history")
    
    def __repr__(self):
        return f"<ChatHistory(id={self.id}, user_id={self.user_id}, role={self.role})>"


class APIKey(Base):
    """API keys for programmatic access"""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    key_hash = Column(String, nullable=False, unique=True, index=True)
    name = Column(String)  # Friendly name for the key
    
    # Permissions
    scopes = Column(JSON)  # List of allowed scopes
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime)
    last_used = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    
    def __repr__(self):
        return f"<APIKey(id={self.id}, user_id={self.user_id}, name={self.name})>"


class UserSession(Base):
    """Active user sessions"""
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    session_token = Column(String, unique=True, nullable=False, index=True)
    
    # Session data
    ip_address = Column(String)
    user_agent = Column(String)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=False)
    last_activity = Column(DateTime, default=datetime.now(timezone.utc))
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id})>"


class AuditLog(Base):
    """Audit trail for security and compliance"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True)
    action = Column(String, nullable=False, index=True)
    resource = Column(String)
    details = Column(JSON)
    
    # Request metadata
    ip_address = Column(String)
    user_agent = Column(String)
    
    # Status
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), index=True)
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action}, user_id={self.user_id})>"


class CacheEntry(Base):
    """Database-backed cache for expensive computations"""
    __tablename__ = "cache_entries"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, unique=True, nullable=False, index=True)
    value = Column(JSON, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=False, index=True)
    hit_count = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<CacheEntry(key={self.key})>"


# ── Database Utilities ─────────────────────────────────────────────────────

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Drop all database tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """Context manager for database session"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ── CRUD Operations ────────────────────────────────────────────────────────

def create_user(db: Session, user_data: dict) -> User:
    """Create a new user"""
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: str) -> User:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_name(db: Session, name: str) -> User:
    """Get user by name (case-insensitive)"""
    return db.query(User).filter(User.name.ilike(name)).first()


def update_user(db: Session, user_id: str, updates: dict) -> User:
    """Update user data"""
    user = get_user_by_id(db, user_id)
    if user:
        for key, value in updates.items():
            setattr(user, key, value)
        user.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: str) -> bool:
    """Delete a user"""
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


def save_chat_message(db: Session, user_id: str, role: str, content: str, **metadata) -> ChatHistory:
    """Save a chat message"""
    chat = ChatHistory(
        user_id=user_id,
        role=role,
        content=content,
        **metadata
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_chat_history(db: Session, user_id: str, limit: int = 50) -> list[ChatHistory]:
    """Get chat history for a user"""
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.timestamp.desc())
        .limit(limit)
        .all()
    )


def create_audit_log(db: Session, **log_data) -> AuditLog:
    """Create an audit log entry"""
    log = AuditLog(**log_data)
    db.add(log)
    db.commit()
    return log
