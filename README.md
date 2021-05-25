# applifting
This is an API for an exercise for Applifting. To start my program you have to set up a few things. 
First, you need to install Python 3.8.6 or a later version. Then clone this repository from GitHub. Also, you should create venv using this command (you should enter this command from directory with files of this project):

python3 -m venv venv

and install external libraries by next command, which will be used in this project: 

pip install -r requirements.txt

The next step is to create an environment variable. A template of .env file is in the repository(.env.distr).

Also you need to set up your crontab with settings "*/1 * * * *". 

In order for API to be deployed on your local server you have to start a server.py file via the following command:

python3 classes.py
python3 server.py

Now API is deployed and you can start using it(default local url is "http://127.0.0.1:5000/").

For testing use a "classes_test.py" file and pytest library.
