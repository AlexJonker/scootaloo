import os
import subprocess
import platform
import string
import random
import json

def run_command(command, shell=False):
    try:
        result = subprocess.run(command, shell=shell, text=True, check=True)
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
    if OS == "Windows":
        run_command("py -m venv .venv", shell=True)
    else:
        run_command("python -m venv .venv", shell=True)
    print("Created .venv")

def create_conf(OS):
    if not os.path.exists("conf.json.example"):
        print("Error: conf.json.example file not found.")
        exit()

    if OS == "Windows":
        run_command("copy conf.json.example conf.json", shell=True)
    else:
        run_command("cp conf.json.example conf.json", shell=True)

def main():
    OS = platform.system()
    if OS not in ["Linux", "Darwin", "Windows"]:
        print("Unsupported OS")
        exit()

    if OS == "Windows":
        activate_cmd = ".\\venv\\Scripts\\activate"
    else:
        activate_cmd = ". .venv/bin/activate"

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
    runserver_cmd = f"{activate_cmd} && django-admin runserver --pythonpath=. --settings=main 0.0.0.0:{port}"

    if OS == "Windows":
        run_command(f'cmd.exe /c "{install_cmd} && {runserver_cmd}"', shell=True)
    else:
        run_command(install_cmd, shell=True)
        run_command(runserver_cmd, shell=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping server...")
        exit()
