import argparse
import secrets

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=8000)
args = parser.parse_args()

# Generate a new secret key
secret_key = secrets.token_hex(32)

# Write secret key and port to .env file
with open(".env", "w") as f:
    f.write(f"SECRET_KEY={secret_key}\n")
    f.write(f"PORT={args.port}\n")

print("Secret key and port written to .env file")
