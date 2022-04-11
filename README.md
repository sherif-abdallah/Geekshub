# Geekshub

New Social Media Platform

## Steps to install the platform


#### Create Virtual enviroumunt if there isn't For Linux or MacOs
```bash
py -m venv venv
```
#### Create Virtual enviroumunt if there isn't
```bash
python3 -m venv venv
```
#### Activate the Virtual enviroumunt For Linux or MacOs
```bash
source venv/bin/activate.bat
```
#### Activate the Virtual enviroumunt For Windows
```bash
venv\Scripts\activate
```
#### Download PIP For Windows From The Following Link [Download PIP](https://bootstrap.pypa.io/get-pip.py)
```bash
py get-pip.py
```
#### Download PIP For Linux or MacOs
```bash
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
```
#### Install Project Required Packages and libraries
```bash
pip install -r requirements.txt
```
#### Migrate the Database on Windows
```bash
py manage.py migrate --run-syncdb
```
#### Migrate the Database on Linux or Macos
```bash
python3 manage.py migrate --run-syncdb
```
#### Run The Platform Sever on Windows
```bash
py manage.py runserver
```
###### Change The All Secret Variables  in .env file


#### Run The Platform Sever on Linux or Macos
```bash
python3 manage.py runserver
```
