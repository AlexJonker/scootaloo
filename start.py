import subprocess
import platform
try:

    # Determine the OS
    OS = platform.system()

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


    # Function to run a shell command
    def run_command(command, shell=True):
        result = subprocess.run(command, shell=shell, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
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