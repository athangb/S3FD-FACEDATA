import os

def check_directory_exists(directory):
    return os.path.exists(directory)

def create_directories(directories):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def install_package(package_name):
    import subprocess
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", package_name])
