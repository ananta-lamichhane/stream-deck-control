import subprocess

def open_application(application):
    try:
        subprocess.run([f"{application}"], check=True)
        print(f"{application} opened successfully.")
    except FileNotFoundError:
        print(f"{application} is not installed or not in the system PATH.")
    except subprocess.CalledProcessError:
        print(f"An error occurred while trying to open {application}.")

# # Call the function
# open_vscode()

