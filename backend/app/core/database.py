# Mock database for development - no external dependencies
import logging

logger = logging.getLogger(__name__)

# Mock storage for development
mock_todos = []
mock_users = []

def get_mock_storage():
    """Return mock storage for development"""
    return {
        'todos': mock_todos,
        'users': mock_users
    }

# Convenience function for backward compatibility
def get_supabase_client():
    """Returns None - using mock storage instead"""
    return None