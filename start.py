import os
import subprocess
import platform
import string
import random
import json

def run_command(command):
    try:
        subprocess.run(command, shell=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}\n{e}")
        exit()

def create_env_file():
    print("Warning: .env file not found. Creating one now...")
    size = 69
    chars = string.ascii_letters + string.digits + string.punctuation
    SECRET_KEY = ''.join(random.choice(chars) for _ in range(size))
    with open(".env", "w") as f:
        f.write(f"SECRET_KEY={SECRET_KEY}")
    print("Created .env")

def create_virtualenv(OS):
    print("Virtual environment not found. Creating one...")
    run_command("python -m venv .venv" if OS in ["Linux", "Darwin"] else "py -m venv .venv")
    print("Created .venv")

def create_conf(OS):
    run_command("cp conf.json.example conf.json" if OS in ["Linux", "Darwin"] else "copy conf.json.example conf.json")

def main():
    OS = platform.system()
    if OS not in ["Linux", "Darwin", "Windows"]:
        print("Unsupported OS")
        exit()

    activate_cmd = ". .venv/bin/activate" if OS in ["Linux", "Darwin"] else ".venv\\Scripts\\activate"

    if not os.path.exists(".env"):
        create_env_file()

    if not os.path.exists(".venv"):
        create_virtualenv(OS)

    if not os.path.exists("conf.json"):
        create_conf(OS)

    with open('conf.json', 'r') as file:
        conf = json.load(file)

    port = conf["port"]
    install_cmd = f"{activate_cmd} && pip install -r requirements.txt"
    runserver_cmd = f"{activate_cmd} && django-admin runserver --pythonpath=. --settings=main {port}"

    if OS == "Windows":
        run_command(f'cmd.exe /c "{install_cmd} && {runserver_cmd}"')
    else:
        run_command(install_cmd)
        run_command(runserver_cmd)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping server...")
        exit()