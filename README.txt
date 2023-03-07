# Project Setup
- Install Python3.10 or above on your system if not already installed.
Venv For Windows:-
- Create virtualenv: python -m venv venv
- Activate virtualenv: source .\venv\Scripts\activate
- Install dependincies: pip install -r requirements.txt
 
# Database
 - Using sqlite database
 - Run init command only first time to iniatlize database(database.db) and migrations folder.
   flask db init

- Run these cmds everytime you make changes in models
  flask db migrate
  flask db upgrade

# Run Server
cd notes/ 
flask run

Visit: http://localhost:5000


# Webapp Default Test User Login:
email: test@gmail.com
password: test@123


──────▄▀▄─────▄▀▄
─────▄█░░▀▀▀▀▀░░█▄
─▄▄──█░░░░░░░░░░░█──▄▄
█▄▄█─█░░▀░░┬░░▀░░█─█▄▄█
