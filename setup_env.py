import os
import subprocess
import sys

def create_and_activate_venv():
    # Create virtual environment
    subprocess.check_call([sys.executable, '-m', 'venv', '.venv'])
    
    # Activate virtual environment
    if os.name == 'nt':
        activate_script = '.venv\\Scripts\\activate.bat'
    else:
        activate_script = '.venv/bin/activate'
    
    # Install dependencies
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

if __name__ == '__main__':
    create_and_activate_venv()
