import os
import subprocess
import platform
import string
import random

try:

    # Determine the OS
    OS = platform.system()


    # Function to run a shell command
    def run_command(command, shell=True):
        result = subprocess.run(command, shell=shell, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            exit()


    # Check if virtual environment exists
    if not os.path.exists(".venv"):
        print("Virtual environment not found. Creating one...")
        run_command("python -m venv .venv")



    # Define the virtual environment activation command
    if OS in ["Linux", "Darwin"]:
        print(f"Activating venv for {OS}")
        activate_cmd = "source .venv/bin/activate"
    elif OS == "Windows":
        print(f"Activating venv for {OS}")
        activate_cmd = ".venv\\Scripts\\activate"
    else:
        print("Unsupported OS")
        exit()

    # Check if .env file exists
    if not os.path.exists(".env"):
        print("Warning: .env file not found. Creating one now...")
        f = open(".env", "a")

        size = 69
        chars = string.ascii_letters + string.digits + string.punctuation
        SECRET_KEY = ''.join(c.lower() if random.choice([True, False]) else c for c in (random.choice(chars) for _ in range(size)))

        SECRET_KEY = SECRET_KEY
        f.write(f"SECRET_KEY={SECRET_KEY}")
        exit()

    # Activate virtual environment
    if OS == "Windows":
        venv_cmd = f'cmd.exe /c "{activate_cmd} && pip install -r requirements.txt && python manage.py makemigrations && python manage.py migrate && python manage.py runserver"'
        subprocess.run(venv_cmd, shell=True)
    else:
        commands = [
            f"{activate_cmd} && pip install -r requirements.txt",
            f"{activate_cmd} && python manage.py makemigrations",
            f"{activate_cmd} && python manage.py migrate",
            f"{activate_cmd} && python manage.py runserver"
        ]

        for cmd in commands:
            run_command(cmd)


except KeyboardInterrupt as e:
    print("\nStopping server...")
    exit()