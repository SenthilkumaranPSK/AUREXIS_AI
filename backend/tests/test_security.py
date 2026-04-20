"""
Test Security Module
"""

import pytest
from security import (
    hash_password,
    verify_password,
    validate_password_strength,
    create_access_token,
    decode_token,
    generate_api_key,
    sanitize_input,
    validate_user_id,
)


def test_password_hashing():
    """Test password hashing and verification"""
    password = "TestPassword123!"
    hashed = hash_password(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword", hashed)


def test_password_strength_validation():
    """Test password strength validation"""
    # Valid password
    is_valid, msg = validate_password_strength("StrongPass@123")
    assert is_valid
    assert msg == ""
    
    # Too short
    is_valid, msg = validate_password_strength("Short1!")
    assert not is_valid
    assert "at least" in msg.lower()
    
    # No uppercase
    is_valid, msg = validate_password_strength("lowercase123!")
    assert not is_valid
    assert "uppercase" in msg.lower()
    
    # No lowercase
    is_valid, msg = validate_password_strength("UPPERCASE123!")
    assert not is_valid
    assert "lowercase" in msg.lower()
    
    # No digit
    is_valid, msg = validate_password_strength("NoDigits!")
    assert not is_valid
    assert "digit" in msg.lower()
    
    # No special character
    is_valid, msg = validate_password_strength("NoSpecial123")
    assert not is_valid
    assert "special" in msg.lower()


def test_jwt_token_creation_and_decoding():
    """Test JWT token creation and decoding"""
    data = {"sub": "1010101010", "name": "Test User"}
    token = create_access_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Decode token
    payload = decode_token(token)
    assert payload["sub"] == "1010101010"
    assert payload["name"] == "Test User"
    assert "exp" in payload
    assert "iat" in payload
    assert payload["type"] == "access"


def test_api_key_generation():
    """Test API key generation"""
    key1 = generate_api_key()
    key2 = generate_api_key()
    
    assert isinstance(key1, str)
    assert isinstance(key2, str)
    assert len(key1) > 20
    assert key1 != key2  # Should be unique


def test_input_sanitization():
    """Test input sanitization"""
    # Remove null bytes
    assert sanitize_input("test\x00data") == "testdata"
    
    # Trim whitespace
    assert sanitize_input("  test  ") == "test"
    
    # Limit length
    long_text = "a" * 2000
    assert len(sanitize_input(long_text, max_length=100)) == 100


def test_user_id_validation():
    """Test user ID validation"""
    assert validate_user_id("1010101010")
    assert not validate_user_id("123")  # Too short
    assert not validate_user_id("abcdefghij")  # Not digits
    assert not validate_user_id("12345678901")  # Too long
