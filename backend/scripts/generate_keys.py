"""
Generate secure random keys for .env file
Run this script to generate SECRET_KEY and JWT_SECRET_KEY
"""
import secrets

print("=" * 60)
print("SECURE KEY GENERATOR")
print("=" * 60)
print("\nGenerating secure random keys...\n")

secret_key = secrets.token_urlsafe(32)
jwt_secret_key = secrets.token_urlsafe(32)

print("Copy these values to your .env file:")
print("-" * 60)
print(f"SECRET_KEY={secret_key}")
print(f"JWT_SECRET_KEY={jwt_secret_key}")
print("-" * 60)

print("\nTo use these keys:")
print("1. Create a file named '.env' in the backend folder")
print("2. Copy the lines above into the .env file")
print("3. Restart your server")
print("\n⚠️  IMPORTANT: Never commit .env file to git!")
print("=" * 60)
