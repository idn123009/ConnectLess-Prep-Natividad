@echo off

:: Step 1: Create a virtual environment
echo Creating virtual environment...
python -m venv .venv

:: Step 2: Activate the virtual environment (for Command Prompt)
echo Activating virtual environment...
call .venv\Scripts\activate.bat

:: Step 3: Install dependencies from requirements.txt
echo Installing dependencies from requirements.txt...
pip install --upgrade pip  # Ensure pip is up to date
pip install -r requirements.txt

:: Step 4: Run the Django development server
echo Running Django web app...
python manage.py runserver
echo Setup and server started successfully!

pause