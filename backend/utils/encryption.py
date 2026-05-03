"""
Data Encryption Utilities for Sensitive Information
"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import base64
import json
from typing import Any, Dict, Optional
import os


class DataEncryption:
    """Handle encryption/decryption of sensitive data"""
    
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize encryption with key
        
        Args:
            encryption_key: Base64 encoded Fernet key. If None, generates new key.
        """
        if encryption_key:
            self.key = encryption_key.encode()
        else:
            # Generate key from environment or create new
            self.key = os.getenv("DATA_ENCRYPTION_KEY", Fernet.generate_key().decode()).encode()
        
        try:
            self.cipher = Fernet(self.key)
        except Exception as e:
            raise ValueError(f"Invalid encryption key: {e}")
    
    def encrypt_string(self, data: str) -> str:
        """
        Encrypt a string
        
        Args:
            data: Plain text string
            
        Returns:
            Base64 encoded encrypted string
        """
        if not data:
            return data
        
        encrypted = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt_string(self, encrypted_data: str) -> str:
        """
        Decrypt a string
        
        Args:
            encrypted_data: Base64 encoded encrypted string
            
        Returns:
            Decrypted plain text string
        """
        if not encrypted_data:
            return encrypted_data
        
        try:
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")
    
    def encrypt_dict(self, data: Dict[str, Any], fields: list) -> Dict[str, Any]:
        """
        Encrypt specific fields in a dictionary
        
        Args:
            data: Dictionary containing data
            fields: List of field names to encrypt
            
        Returns:
            Dictionary with encrypted fields
        """
        encrypted_data = data.copy()
        
        for field in fields:
            if field in encrypted_data and encrypted_data[field]:
                encrypted_data[field] = self.encrypt_string(str(encrypted_data[field]))
        
        return encrypted_data
    
    def decrypt_dict(self, data: Dict[str, Any], fields: list) -> Dict[str, Any]:
        """
        Decrypt specific fields in a dictionary
        
        Args:
            data: Dictionary containing encrypted data
            fields: List of field names to decrypt
            
        Returns:
            Dictionary with decrypted fields
        """
        decrypted_data = data.copy()
        
        for field in fields:
            if field in decrypted_data and decrypted_data[field]:
                try:
                    decrypted_data[field] = self.decrypt_string(decrypted_data[field])
                except Exception:
                    # If decryption fails, data might not be encrypted
                    pass
        
        return decrypted_data
    
    def encrypt_json_file(self, file_path: str, sensitive_fields: list):
        """
        Encrypt sensitive fields in a JSON file
        
        Args:
            file_path: Path to JSON file
            sensitive_fields: List of field names to encrypt
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Encrypt sensitive fields
            encrypted_data = self.encrypt_dict(data, sensitive_fields)
            
            # Write back to file
            with open(file_path, 'w') as f:
                json.dump(encrypted_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error encrypting file {file_path}: {e}")
            return False
    
    def decrypt_json_file(self, file_path: str, sensitive_fields: list) -> Dict:
        """
        Decrypt sensitive fields in a JSON file
        
        Args:
            file_path: Path to JSON file
            sensitive_fields: List of field names to decrypt
            
        Returns:
            Decrypted data dictionary
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Decrypt sensitive fields
            return self.decrypt_dict(data, sensitive_fields)
        except Exception as e:
            print(f"Error decrypting file {file_path}: {e}")
            return {}
    
    @staticmethod
    def generate_key() -> str:
        """Generate a new Fernet key"""
        return Fernet.generate_key().decode()
    
    @staticmethod
    def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
        """
        Mask sensitive data for logging/display
        
        Args:
            data: Sensitive string to mask
            visible_chars: Number of characters to show at end
            
        Returns:
            Masked string (e.g., "****1234")
        """
        if not data or len(data) <= visible_chars:
            return "****"
        
        return "*" * (len(data) - visible_chars) + data[-visible_chars:]


# Sensitive fields that should be encrypted
SENSITIVE_FIELDS = [
    "account_number",
    "accountNumber",
    "bank_account",
    "credit_card",
    "ssn",
    "tax_id",
    "password",
    "secret",
    "token",
    "api_key",
    "private_key"
]


def get_encryption_service() -> DataEncryption:
    """Get encryption service instance"""
    from config_manager import get_settings
    settings = get_settings()
    
    key = None
    if settings.data_encryption_key:
        key = settings.data_encryption_key.get_secret_value()
    
    return DataEncryption(key)
