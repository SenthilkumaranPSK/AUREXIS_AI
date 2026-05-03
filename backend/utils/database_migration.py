"""
Database Migration Utilities
Migrate from JSON to PostgreSQL/SQLite
"""
import json
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

logger = logging.getLogger(__name__)


class DatabaseMigration:
    """Handle migration from JSON to database"""
    
    def __init__(self, database_url: str, json_data_dir: str = "./backend/user_data"):
        self.database_url = database_url
        self.json_data_dir = Path(json_data_dir)
        self.engine = None
        self.session_maker = None
    
    async def initialize(self):
        """Initialize database connection"""
        self.engine = create_async_engine(
            self.database_url,
            echo=False,
            future=True
        )
        
        self.session_maker = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        logger.info(f"Database connection initialized: {self.database_url}")
    
    async def create_tables(self):
        """Create database tables"""
        from sqlalchemy import MetaData
        from sqlalchemy.ext.declarative import declarative_base
        
        Base = declarative_base()
        
        # Import models here to register them
        # from models import User, Transaction, Budget, etc.
        
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database tables created")
    
    async def migrate_user_data(self, user_id: str) -> bool:
        """
        Migrate single user's data from JSON to database
        
        Args:
            user_id: User account number
            
        Returns:
            True if successful
        """
        user_dir = self.json_data_dir / user_id
        
        if not user_dir.exists():
            logger.warning(f"User directory not found: {user_id}")
            return False
        
        try:
            logger.info(f"Migrating user: {user_id}")
            
            # Read profile
            profile_path = user_dir / "profile.json"
            if profile_path.exists():
                with open(profile_path, 'r') as f:
                    profile_data = json.load(f)
                await self._migrate_profile(profile_data)
            
            # Read transactions
            transactions_path = user_dir / "fetch_bank_transactions.json"
            if transactions_path.exists():
                with open(transactions_path, 'r') as f:
                    transactions_data = json.load(f)
                await self._migrate_transactions(user_id, transactions_data)
            
            # Read investments
            stocks_path = user_dir / "fetch_stock_transactions.json"
            if stocks_path.exists():
                with open(stocks_path, 'r') as f:
                    stocks_data = json.load(f)
                await self._migrate_investments(user_id, stocks_data, "stock")
            
            mf_path = user_dir / "fetch_mf_transactions.json"
            if mf_path.exists():
                with open(mf_path, 'r') as f:
                    mf_data = json.load(f)
                await self._migrate_investments(user_id, mf_data, "mutual_fund")
            
            # Read credit report
            credit_path = user_dir / "fetch_credit_report.json"
            if credit_path.exists():
                with open(credit_path, 'r') as f:
                    credit_data = json.load(f)
                await self._migrate_credit_data(user_id, credit_data)
            
            logger.info(f"Successfully migrated user: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Migration failed for user {user_id}: {e}")
            return False
    
    async def _migrate_profile(self, profile_data: Dict):
        """Migrate user profile"""
        async with self.session_maker() as session:
            # Insert user profile
            query = text("""
                INSERT INTO users (
                    id, name, email, occupation, age, location,
                    monthly_income, monthly_expense, net_worth,
                    credit_score, savings_rate, risk_level,
                    created_at, updated_at
                ) VALUES (
                    :id, :name, :email, :occupation, :age, :location,
                    :monthly_income, :monthly_expense, :net_worth,
                    :credit_score, :savings_rate, :risk_level,
                    :created_at, :updated_at
                )
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    email = EXCLUDED.email,
                    updated_at = EXCLUDED.updated_at
            """)
            
            await session.execute(query, {
                "id": profile_data.get("id"),
                "name": profile_data.get("name"),
                "email": profile_data.get("email"),
                "occupation": profile_data.get("occupation"),
                "age": profile_data.get("age"),
                "location": profile_data.get("location"),
                "monthly_income": profile_data.get("monthlyIncome", 0),
                "monthly_expense": profile_data.get("monthlyExpense", 0),
                "net_worth": profile_data.get("netWorth", 0),
                "credit_score": profile_data.get("creditScore", 0),
                "savings_rate": profile_data.get("savingsRate", 0),
                "risk_level": profile_data.get("riskLevel", "Medium"),
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            })
            
            await session.commit()
    
    async def _migrate_transactions(self, user_id: str, transactions_data: Dict):
        """Migrate bank transactions"""
        async with self.session_maker() as session:
            bank_transactions = transactions_data.get("bankTransactions", [])
            
            for bank_data in bank_transactions:
                bank_name = bank_data.get("bank")
                txns = bank_data.get("txns", [])
                
                for txn in txns:
                    # Parse transaction array
                    amount, narration, date, txn_type, mode, balance = txn
                    
                    # Map transaction type
                    type_map = {1: "CREDIT", 2: "DEBIT", 4: "INTEREST", 6: "INSTALLMENT"}
                    transaction_type = type_map.get(txn_type, "OTHER")
                    
                    query = text("""
                        INSERT INTO transactions (
                            user_id, amount, description, date, type,
                            category, mode, balance, bank_name,
                            created_at
                        ) VALUES (
                            :user_id, :amount, :description, :date, :type,
                            :category, :mode, :balance, :bank_name,
                            :created_at
                        )
                    """)
                    
                    await session.execute(query, {
                        "user_id": user_id,
                        "amount": float(amount),
                        "description": narration,
                        "date": date,
                        "type": transaction_type,
                        "category": self._extract_category(narration),
                        "mode": mode,
                        "balance": float(balance),
                        "bank_name": bank_name,
                        "created_at": datetime.now()
                    })
            
            await session.commit()
    
    async def _migrate_investments(self, user_id: str, investment_data: Dict, investment_type: str):
        """Migrate investment data"""
        # Implementation for investment migration
        pass
    
    async def _migrate_credit_data(self, user_id: str, credit_data: Dict):
        """Migrate credit report data"""
        # Implementation for credit data migration
        pass
    
    def _extract_category(self, narration: str) -> str:
        """Extract category from transaction narration"""
        narration_lower = narration.lower()
        
        if any(word in narration_lower for word in ["salary", "income"]):
            return "Income"
        elif any(word in narration_lower for word in ["rent", "landlord"]):
            return "Housing"
        elif any(word in narration_lower for word in ["grocer", "food", "swiggy", "zomato"]):
            return "Food"
        elif any(word in narration_lower for word in ["electricity", "water", "gas", "bescom", "tneb"]):
            return "Utilities"
        elif any(word in narration_lower for word in ["petrol", "fuel", "transport"]):
            return "Transportation"
        elif any(word in narration_lower for word in ["mutualfund", "sip", "investment"]):
            return "Investment"
        elif any(word in narration_lower for word in ["credit card", "card payment"]):
            return "Credit Card"
        elif any(word in narration_lower for word in ["recharge", "mobile", "airtel", "jio"]):
            return "Utilities"
        else:
            return "Other"
    
    async def migrate_all_users(self) -> Dict[str, Any]:
        """
        Migrate all users from JSON to database
        
        Returns:
            Migration statistics
        """
        stats = {
            "total_users": 0,
            "successful": 0,
            "failed": 0,
            "failed_users": []
        }
        
        # Get all user directories
        user_dirs = [d for d in self.json_data_dir.iterdir() if d.is_dir()]
        stats["total_users"] = len(user_dirs)
        
        logger.info(f"Starting migration for {stats['total_users']} users")
        
        for user_dir in user_dirs:
            user_id = user_dir.name
            
            try:
                success = await self.migrate_user_data(user_id)
                
                if success:
                    stats["successful"] += 1
                else:
                    stats["failed"] += 1
                    stats["failed_users"].append(user_id)
            except Exception as e:
                logger.error(f"Error migrating user {user_id}: {e}")
                stats["failed"] += 1
                stats["failed_users"].append(user_id)
        
        logger.info(f"Migration complete: {stats['successful']}/{stats['total_users']} successful")
        
        return stats
    
    async def verify_migration(self, user_id: str) -> Dict[str, Any]:
        """
        Verify migration for a user
        
        Returns:
            Verification results
        """
        results = {
            "user_id": user_id,
            "profile_exists": False,
            "transaction_count": 0,
            "investment_count": 0,
            "issues": []
        }
        
        async with self.session_maker() as session:
            # Check profile
            profile_query = text("SELECT COUNT(*) FROM users WHERE id = :user_id")
            result = await session.execute(profile_query, {"user_id": user_id})
            results["profile_exists"] = result.scalar() > 0
            
            # Check transactions
            txn_query = text("SELECT COUNT(*) FROM transactions WHERE user_id = :user_id")
            result = await session.execute(txn_query, {"user_id": user_id})
            results["transaction_count"] = result.scalar()
            
            # Check investments
            inv_query = text("SELECT COUNT(*) FROM investments WHERE user_id = :user_id")
            result = await session.execute(inv_query, {"user_id": user_id})
            results["investment_count"] = result.scalar()
        
        return results
    
    async def close(self):
        """Close database connection"""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connection closed")


# CLI interface for migration
async def run_migration(database_url: str, json_data_dir: str = "./backend/user_data"):
    """Run database migration"""
    migration = DatabaseMigration(database_url, json_data_dir)
    
    try:
        await migration.initialize()
        await migration.create_tables()
        
        stats = await migration.migrate_all_users()
        
        print("\n" + "="*60)
        print("MIGRATION COMPLETE")
        print("="*60)
        print(f"Total users: {stats['total_users']}")
        print(f"Successful: {stats['successful']}")
        print(f"Failed: {stats['failed']}")
        
        if stats['failed_users']:
            print(f"\nFailed users: {', '.join(stats['failed_users'])}")
        
        print("="*60 + "\n")
        
    finally:
        await migration.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python database_migration.py <database_url>")
        print("Example: python database_migration.py postgresql+asyncpg://user:pass@localhost/aurexis")
        sys.exit(1)
    
    database_url = sys.argv[1]
    asyncio.run(run_migration(database_url))
