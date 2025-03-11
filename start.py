import os
import subprocess
import platform
import string
import random
import json

def run_command(command, shell=False):
    try:
        subprocess.run(command, shell=shell, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}\n{e}")
        exit(1)

def create_env_file():
    print("Warning: .env file not found. Creating one now...")
    size = 69
    chars = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(random.choice(chars) for _ in range(size))
    with open(".env", "w") as f:
        f.write(f"SECRET_KEY={secret_key}")
    print("Created .env")

def create_virtualenv(os_name):
    print("Virtual environment not found. Creating one...")
    command = "py -m venv .venv" if os_name == "Windows" else "python -m venv .venv"
    run_command(command, shell=True)
    print("Created .venv")

def create_conf(os_name):
    if not os.path.exists("conf.json.example"):
        print("Error: conf.json.example file not found.")
        exit(1)

    command = "copy conf.json.example conf.json" if os_name == "Windows" else "cp conf.json.example conf.json"
    run_command(command, shell=True)

def main():
    os_name = platform.system()
    if os_name not in ["Linux", "Darwin", "Windows"]:
        print("Unsupported OS")
        exit(1)

    activate_cmd = ".\\venv\\Scripts\\activate" if os_name == "Windows" else ". .venv/bin/activate"

    if not os.path.exists(".env"):
        create_env_file()

    if not os.path.exists(".venv"):
        create_virtualenv(os_name)

    if not os.path.exists("conf.json"):
        create_conf(os_name)

    with open('conf.json', 'r') as file:
        conf = json.load(file)

    port = conf["port"]
    install_cmd = f"{activate_cmd} && pip install -r requirements.txt"
    runserver_cmd = f"{activate_cmd} && django-admin runserver --pythonpath=. --settings=main 0.0.0.0:{port}"

    if os_name == "Windows":
        run_command(f'cmd.exe /c "{install_cmd} && {runserver_cmd}"', shell=True)
    else:
        run_command(install_cmd, shell=True)
        run_command(runserver_cmd, shell=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping server...")
        exit(0)
