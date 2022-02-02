# wlobby_backend
Backend of wlobby app

## Build
1. Create an empty folder and go into that folder.
2. Create a virtual environment with `python -m venv my_virtual_env` command. Replace your actual virtual environment name to `my_virtual_env`
3. Put `my_virtual_env/` under the `Virtual Environments` part of `.gitignore` file. In this way, you will not push your virtual environment directory.
   Replace your actual virtual environment name to `my_virtual_env` Note: If you re-build this project and your environment name is already in the `.gitignore` file, 
   then you do not have to add the same name again you can skip this step. 
4. Activate your virtual environment with `.\my_virtual_env\Scripts\activate` command. Again replace your actual virtual environment name to `my_virtual_env`
5. Install all dependencies with `python -m pip install -r .\src\requirements.txt` command.
6. Create a file named `"access_keys.txt"` under the `src` folder. 
7. Put your access key to the first line and secret access key to the second line of `"access_keys.txt"` file.
8. Test your API connection with `python dynamodb.py` command. Note: You must be inside the `src` folder.
   If this command prints some data to console you are good, otherwise check previous steps.
9. Test your Django build with `python manage.py runserver` command. Note: You must be inside the `src` folder.
   If this command gives you the local host URL you are good, otherwise check previous steps.
   
If you can achieve all these steps with no errors, then you are all set.
   
