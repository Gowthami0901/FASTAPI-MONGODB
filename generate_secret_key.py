import secrets

def generate_secret_key():
    return secrets.token_urlsafe(32)

# Generate a secret key
if __name__ == "__main__":
    secret_key = generate_secret_key()
    print(secret_key)
