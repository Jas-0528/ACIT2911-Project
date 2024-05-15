import secrets

# Generate a new secret key
secret_key = secrets.token_hex(32)

# Write secret key to .env file
with open(".env", "w") as f:
    f.write(f"SECRET_KEY={secret_key}\n")

print("Secret key written to .env file.")
