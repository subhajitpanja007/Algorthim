@echo off

REM Set the environment variable to allow the Python launcher to use winget
set PYLAUNCHER_ALLOW_INSTALL=1

REM Set the Python path and update PATH environment variable
set PYTHONPATH=C:\Users\Subhajit Panja\AppData\Local\Programs\Python\Python310\Lib
set PATH=C:\Users\Subhajit Panja\AppData\Local\Programs\Python\Python310;C:\Users\Subhajit Panja\AppData\Local\Programs\Python\Python310\Scripts;%PATH%

REM List all Python versions installed
py --list

REM Create the virtual environment with the specified Python version using the full path
"C:\Users\Subhajit Panja\AppData\Local\Programs\Python\Python310\python.exe" -m venv .venv

REM Check if the virtual environment was created successfully
if exist ".venv\Scripts\activate" (
    echo Virtual environment created successfully.
    
    REM Activate the virtual environment
    call .venv\Scripts\activate
    
    REM Check the Python version to confirm the correct environment is active
    python --version
    
    REM Upgrade pip
    python -m pip install --upgrade pip
    
    REM Install packages from requirements.txt
    if exist requirements.txt (
        pip install -r requirements.txt
    ) else (
        echo requirements.txt not found.
    )
) else (
    echo Failed to create virtual environment.
    echo Please ensure Python 3.10.9 is installed and accessible.
)

REM Explanation of the pause command:
REM The pause command is used to keep the Command Prompt window open after the batch file has finished executing.
REM This way, you can see the output and any messages displayed, rather than the window closing immediately.
REM When pause is encountered, it displays the message "Press any key to continue . . ." and waits for you to press a key before proceeding, ensuring you can review the script’s output.

pause
