# wlobby_backend
Backend of wlobby app

## Build
1.  Create an empty folder and go into that folder.
2.  Create a virtual environment with `python -m venv my_virtual_env` command. Replace your actual virtual environment name to `my_virtual_env`
3.  Put `my_virtual_env/` under the `Virtual Environments` part of `.gitignore` file. In this way, you will not push your virtual environment directory.
    Replace your actual virtual environment name to `my_virtual_env` Note: If you re-build this project and your environment name is already in the `.gitignore` file, 
    then you do not have to add the same name again you can skip this step. 
4.  Activate your virtual environment with `.\my_virtual_env\Scripts\activate` command. Again replace your actual virtual environment name to `my_virtual_env`
5.  Install all dependencies with `python -m pip install -r requirements.txt` command.
6.  You must also install pywin32 and pypiwin32 packages with `python -m pip install pywin32` and ` python -m pip install pypiwin32` commands. 
    We cannot add these packages to requirements.txt because these are Windows packages and they don't work on Heroku.
7.  Create a file named `"access_keys.txt"` under the `src` folder. 
8.  Put your access key to the first line and secret access key to the second line of `"access_keys.txt"` file.
9.  Test your API connection with `python dynamodb.py` command. Note: You must be inside the `src` folder.
    If this command prints some data to console you are good, otherwise check previous steps.
10. Test your Django build with `python manage.py runserver` command. Note: You must be inside the `src` folder.
    If this command gives you the local host URL you are good, otherwise check previous steps.
   
If you can achieve all these steps with no errors, then you are all set.

Note: If you install extra packages, you must run `python -m pip freeze > requirements.txt` command in the root directory of project.
      And you must manually delete `pywin32` and `pypiwin32` packages in requirements.txt
      
Note: See the comments in `urls.py` file. You may need to comment out a few lines of code.

Note: You can reach Django REST Swagger Documentation [here](https://django-rest-swagger.readthedocs.io/en/latest/).
      Since we don't have any apps or views in our project right now it is useless for now. 
   
