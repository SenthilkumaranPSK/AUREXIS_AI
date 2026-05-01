"""
Legacy compatibility wrapper for user_manager_secure.
Provides the original public API expected by older code and tests.
"""

# Re-export selected functions from the secure implementation
# Use absolute import to avoid relative import errors when the module is executed as a script
from user_manager_secure import (
    get_all_user_data,
    get_all_users,
    authenticate_user,
)

__all__ = [
    "get_all_user_data",
    "get_all_users",
    "authenticate_user",
]
