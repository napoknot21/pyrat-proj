import os
import subprocess

# Relative path to the PROJECT directory from the current location (PROJECT/extras/)
PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

def run_command(command, cwd=None, silent=False):
    """Run a shell command."""
    process = subprocess.Popen(
        command, cwd=cwd,
        stderr=(subprocess.DEVNULL if silent else None)
    )
    process.communicate()

def main():
    # Ensure we're in the PROJECT directory
    os.chdir(PROJECT_DIR)

    # Create a virtual environment in the PROJECT directory
    run_command(["python3", "-m", "venv", "."])

    # Modify the pyvenv.cfg file
    with open("pyvenv.cfg", "r") as file:
        content = file.read().replace("false", "true")

    with open("pyvenv.cfg", "w") as file:
        file.write(content)

    # Path to the pip and python binaries inside the virtual environment
    pip_bin = os.path.join(PROJECT_DIR, "bin", "pip")
    python_bin = os.path.join(PROJECT_DIR, "bin", "python")

    # Install the PyRat package
    run_command([pip_bin, "install", "./extras/PyRat"])

    # Run the setup_workspace function from the pyrat module
    run_command(
        [python_bin, "-c", "import pyrat; pyrat.PyRat.setup_workspace()"],
        silent=True
    )

if __name__ == "__main__":
    main()
