from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging
import os

logger = logging.getLogger(__name__)

# Database URL - SQLite for local development, PostgreSQL for production
if settings.ENVIRONMENT == "development":
    DATABASE_URL = "sqlite:///./todoShare.db"
else:
    DATABASE_URL = settings.DATABASE_URL or "sqlite:///./todoShare.db"

# SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=settings.ENVIRONMENT == "development"  # Log SQL queries in development
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")

# Convenience function for Supabase compatibility (future migration)
def get_supabase_client():
    """Future: Return Supabase client when migrating"""
    # This will be implemented when migrating to Supabase
    return None