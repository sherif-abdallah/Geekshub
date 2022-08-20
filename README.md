# Geekshub
Geekshub is a Website which allows users, who sign-up for free profiles, to connect with friends, work colleagues or people they don't know, online. It allows users to share pictures, posts, and articles, as well as their own thoughts and opinions with however many people they like.

## Table of Content
- [arabseed-movies-scraper](#arabseed-webscrapping)
  * [Tools](#tools)
  * [How to run](#how-to-run)
  * [Author](#author)

## Tools
1. Python
2. Django (allauth, jazzmin)
3. Mysql Client
4. JavaScript
5. Jquery
6. Ajax
7. Bootstrap


## How to run
* Enter the directory where the script is located then type the following to the console
```sh
$ git clone https://github.com/sherif-abdallah/Geekshub Geekshub
```
* Install Python 3.8 venv, pip and compiler

```sh
$ sudo apt-get install python3.8 python3.8-venv python3-venv
```

* Create a virtual environment to install dependencies in and activate it:

```sh
$ python3.8 -m venv venv
$ source venv/bin/activate
```

* Then install the dependencies:

```sh
(venv)$ cd Geekshub
(venv)$ python -m pip install --upgrade pip
(venv)$ python -m pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

* Once `pip` has finished downloading the dependencies: <br>
Go the `.env` file and Change  `DEBUG = True` `PRODUCTION = False`

then you will have to migrate the db


```sh
(venv)$ python manage.py migrate --run-syncdb
```
* Collect all the static files your are using in all the apps even the third party apps you installed by pip
```sh
(venv)$ python manage.py collectstatic
```

* Finally run The Geekshub Server
```sh
(venv)$ python manage.py runserver
```
* And navigate to `http://127.0.0.1:8000`.

## Author
[Sherif Abdullah](https://github.com/sherif-abdallah)
