"""
Encryption utilities for securing sensitive data like API keys.
Uses Fernet symmetric encryption for secure storage.
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Generate or load encryption key
def get_encryption_key() -> bytes:
    """
    Get or generate encryption key for API key storage.
    In production, this should be stored securely (environment variable, key vault, etc.)
    """
    key_env = os.getenv("ENCRYPTION_KEY")
    if key_env:
        return key_env.encode()
    
    # For development, generate a key based on a password
    # In production, use a proper key management system
    password = os.getenv("ENCRYPTION_PASSWORD", "default-dev-password-change-in-prod").encode()
    salt = b"stable-salt-for-dev"  # In production, use a random salt stored securely
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt_api_key(api_key: str) -> str:
    """
    Encrypt an API key for secure storage.
    
    Args:
        api_key: Plain text API key
        
    Returns:
        Encrypted API key as base64 string
    """
    key = get_encryption_key()
    fernet = Fernet(key)
    encrypted_key = fernet.encrypt(api_key.encode())
    return base64.urlsafe_b64encode(encrypted_key).decode()

def decrypt_api_key(encrypted_api_key: str) -> str:
    """
    Decrypt an API key for use.
    
    Args:
        encrypted_api_key: Encrypted API key as base64 string
        
    Returns:
        Decrypted plain text API key
    """
    key = get_encryption_key()
    fernet = Fernet(key)
    encrypted_data = base64.urlsafe_b64decode(encrypted_api_key.encode())
    decrypted_key = fernet.decrypt(encrypted_data)
    return decrypted_key.decode()

def is_valid_encryption_key(test_value: str = "test") -> bool:
    """
    Test if encryption/decryption is working properly.
    
    Args:
        test_value: Value to test encryption with
        
    Returns:
        True if encryption/decryption works
    """
    try:
        encrypted = encrypt_api_key(test_value)
        decrypted = decrypt_api_key(encrypted)
        return decrypted == test_value
    except Exception:
        return False