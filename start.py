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
    SECRET_KEY = ''.join(c.lower() if random.choice([True, False]) else c for c in (random.choice(chars) for _ in range(size)))
    with open(".env", "w") as f:
        f.write(f"SECRET_KEY={SECRET_KEY}")
    print("Created .env")

def create_virtualenv(OS):
    print("Virtual environment not found. Creating one...")
    if OS in ["Linux", "Darwin"]:
        run_command(["python", "-m", "venv", ".venv"])
    elif OS == "Windows":
        run_command(["py", "-m", "venv", ".venv"])
    print("Created .venv")

def create_conf():
    run_command(["cp conf.json.example conf.json"] if OS in ["Linux", "Darwin"] else ["copy conf.json.example conf.json"], shell=True)

try:
    # Determine the OS
    OS = platform.system()

    # Define the virtual environment activation command
    if OS in ["Linux", "Darwin"]:
        print(f"Activating venv for {OS}")
        activate_cmd = ". .venv/bin/activate"
    elif OS == "Windows":
        print(f"Activating venv for {OS}")
        activate_cmd = ".venv\\Scripts\\activate"
    else:
        print("Unsupported OS")
        exit()

    # Check if .env file exists
    if not os.path.exists(".env"):
        create_env_file()

    # Check if virtual environment exists
    if not os.path.exists(".venv"):
        create_virtualenv(OS)

    if not os.path.exists("conf.json"):
        create_conf()

    with open('conf.json', 'r') as file:
        conf = json.load(file)

    port = conf["port"]

    # Activate virtual environment and run commands
    if OS == "Windows":
        venv_cmd = f'cmd.exe /c "{activate_cmd} && pip install -r requirements.txt && django-admin runserver --pythonpath=. --settings=main 0.0.0.0:{port}"'
        run_command(venv_cmd, shell=True)
    else:
        commands = [
            f"{activate_cmd} && pip install -r requirements.txt",
            f"{activate_cmd} && django-admin runserver --pythonpath=. --settings=main 0.0.0.0:{port}"
        ]

        for cmd in commands:
            run_command(cmd, shell=True)

except KeyboardInterrupt:
    print("\nStopping server...")
    exit()