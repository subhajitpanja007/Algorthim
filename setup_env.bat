@echo off
REM Create virtual environment
python -m venv .venv

REM Activate virtual environment
call .venv\Scripts\activate

REM Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

