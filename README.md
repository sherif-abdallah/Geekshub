# Geekshub

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/sherif-abdallah/Geekshub
```
Install Python 3.8 venv, pip and compiler

```sh
sudo apt-get install python3.8 python3.8-venv python3-venv
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python3.8 -m venv venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(venv)$ cd Geekshub
(venv)$ pip install --upgrade pip
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies: <br>
Go the `social/settings.py` file and Change  `DEBUG = True` `PRODUCTION = False`

then you will have to migrate the db


```sh
(venv)$ python3 manage.py migrate --run-syncdb
```
Collect all the static files your are using in all the apps even the third party apps you installed by pip
```sh
(venv)$ python3 manage.py collectstatic
```

Finally run The Geekshub Server
```sh
(venv)$ python3 manage.py runserver
```
And navigate to `http://127.0.0.1:8000`.
