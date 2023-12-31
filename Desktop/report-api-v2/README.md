[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Django CI](https://github.com/MKA-Nigeria/report-api-v2/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/MKA-Nigeria/report-api-v2/actions/workflows/test.yml)

### Setting up Python

Get Pyenv from here https://github.com/pyenv/pyenv#installation

### For Windows Users 
Install pip with https://pip.pypa.io/en/stable/installation/

- Install python 3.8.0 using pyenv
  ###Note: for window users Install python 3.8.0 manually from https://www.python.org/downloads/release/python-380/  
  
  ```bash
  pyenv install 3.8.0
  ```

- Set python 3.8.0 as the global python version
- Python --version <-- for window users
  
  ```bash
  pyenv global 3.8.0
  ```

#### Setup Virtual Environment

- Install virtualenv using the following code

    ```bash
    pip install virtualenv
    ```
  
- Create a virtual environment using the following code

    ```bash
    virtualenv venv
    ```
  
- Activate the virtual environment using the following code

    ```bash
    source venv/bin/activate
    source venv/Scripts/activate <-- for window users 
    ```

- Install required libraries;
    ```bash
    pip install -r requirements.txt  ### For Window users, you will need to turn off your antivirus before you install the requirement successfully
    ```
Create a .env file in the root directory of the project and copy the contents of .env.example into it
  
### Setting up the database

- Follow the instructions here to install mysql https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/
### Note: Window users should add mysql to their environment variable after installation so that it can work successfully. https://www.youtube.com/watch?v=k5tICunelSU

- Create a new **mysql** database that corresponds to the details in the .env file


###### Note: You must be in the project folder

- Make migrations using the below code

    ```bash 
    python manage.py migrate
    ```
  
- Create a SuperAdmin using the below code

    ```bash
    python manage.py createsuperuser
    ```



- Run the server using the following code

    ```bash 
    python manage.py runserver
    ```

###### Note: Django's default port is **8000**. You can specify port when running the server using this code

#### Link to API doc: http://localhost:8000/docs


### TESTING

- Run the following code to run the tests
- Note: You must be in the project folder
    
    ```bash
    python manage.py test
    ```

### Linting

We use [ruff](https://github.com/astral-sh/ruff) for linting. To lint, run the following command:

- Run the following code to lint the project
  ```bash
  ruff .
  ```

There is a pre-commit hook that runs the linter before every commit. If the linter fails, the commit will be aborted.

- Install the pre-commit hook with:

   ```bash
     pre-commit install
   ```
