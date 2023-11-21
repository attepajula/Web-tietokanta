import os
import secrets
import sys
import subprocess
import platform

def create_virtual_environment(venv_path="venv"):
    """
    Luo virtuaaliympäristön ja asentaa tarvittavat kirjastot.

    :param venv_path: Polku virtuaaliympäristölle (oletusarvo: "venv").
    """
    try:
        # Käytä platform-moduulia oikean aktivoimiskomennon luomiseen
        activate_script = "activate" if platform.system() == "Windows" else "activate"
        activate_path = f"{venv_path}/bin/{activate_script}" if platform.system() != "Windows" else f"{venv_path}/Scripts/{activate_script}"

        # Luo virtuaaliympäristö
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

        # Aktivoi virtuaaliympäristö
        subprocess.run(f"source {activate_path}", check=True, shell=True)

    except subprocess.CalledProcessError as e:
        print(f"Virhe: {e}")

def generate_hash():
    # Generate token
     return secrets.token_hex(16)

def create_env_file():
    # Check if .env is available
    if not os.path.exists(".env"):
        # Ask database URL
        database_url = input("Anna psql-tietokannan osoite: ")
        secret_key = generate_hash()

        # Add env variables to .env
        with open(".env", "w") as env_file:
            env_file.write(f"DATABASE_URL={database_url}\n")
            env_file.write(f"SECRET_KEY={secret_key}\n")

        print(".env-tiedosto on luotu onnistuneesti.")
    else:
        print(".env-tiedosto on jo olemassa.")

def install_required_libraries():
    os.system("pip3 install werkzeug")
    os.system("pip3 install python-dotenv")
    os.system("pip3 install flask")

if __name__ == "__main__":
    create_env_file()
    create_virtual_environment()
    install_required_libraries()