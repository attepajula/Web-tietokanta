import os
import secrets
import venv
import subprocess

def create_virtual_environment(venv_path="venv"):
    try:
        venv.create(venv_path, with_pip=True)

        activate_script = os.path.join(venv_path, "bin", "activate")
        
        # Suorita activate-skripti ja asenna paketit käyttäen täyttä polkua pip-komentoon
        os.system(f"source {activate_script} && {venv_path}/bin/pip install --upgrade pip")
        install_required_libraries()

        print("Virtuaaliympäristö aktivoitu ja paketit asennettu onnistuneesti.")

    except Exception as e:
        print(f"Virhe: {e}")

def generate_hash():
    # Generate token
     return secrets.token_hex(16)

def create_env_file():
    # Check if .env is available
    if not os.path.exists(".env"):
        # Ask database URL
        database_url = input("LUO UUSI TIETOKANTA avaamalla psql: CREATE DATABASE uusi_tietokanta; \nAnna psql-tietokannan osoite: ")
        secret_key = generate_hash()

        # Add env variables to .env
        with open(".env", "w") as env_file:
            env_file.write(f"DATABASE_URL={database_url}\n")
            env_file.write(f"SECRET_KEY={secret_key}\n")

        print(".env-tiedosto on luotu onnistuneesti.")
    else:
        print(".env-tiedosto on jo olemassa.")

def install_required_libraries():
    venv_path = "venv"
    subprocess.run([f"{venv_path}/bin/python", "-m", "pip", "install", "werkzeug"])
    subprocess.run([f"{venv_path}/bin/python", "-m", "pip", "install", "python-dotenv"])
    subprocess.run([f"{venv_path}/bin/python", "-m", "pip", "install", "flask"])
    subprocess.run([f"{venv_path}/bin/python", "-m", "pip", "install", "sqlalchemy"])
    subprocess.run([f"{venv_path}/bin/python", "-m", "pip", "install", "flask_sqlalchemy"])
    subprocess.run([f"{venv_path}/bin/python", "-m", "pip", "install", "psycopg2"])
    subprocess.run([f"{venv_path}/bin/python", "-m", "pip", "install", "dotenv"])


if __name__ == "__main__":
    create_env_file()
    create_virtual_environment()