import os
import secrets

def generate_hash():
    # Generate token
     return secrets.token_hex(16)

def create_env_file():
    # Check if .env is available
    if not os.path.exists('.env'):
        # Ask database URL
        database_url = input("Anna psql-tietokannan osoite: ")
        secret_key = generate_hash()

        # Add env variables to .env
        with open('.env', 'w') as env_file:
            env_file.write(f"DATABASE_URL={database_url}\n")
            env_file.write(f"SECRET_KEY={secret_key}\n")

        print(".env-tiedosto on luotu onnistuneesti.")
    else:
        print(".env-tiedosto on jo olemassa.")

if __name__ == "__main__":
    create_env_file()
