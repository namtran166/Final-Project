# Final Project

Final Project Backend for Got It Onboarding Program.

## Setting up

#### 1. Install and activate virtual environment
Make sure that you already are in root directory of the project before running the following code, which is ~/FinalProject in this case. I am using Python 3.7.3, but other versions of Python are also supported. 
```
$ pip3.7 install virtualenv                       # Replace 3.7 by your Python version
$ virtualenv venv --python=python3.7              # Replace 3.7 by your Python version   
$ source venv/bin/activate             
```
	
#### 2. Install requirements
To install all the required libraries and packages for this project, simply run this command: 
```
pip install -r requirements.txt
```

#### 3. Setup database
Create 3 MySQL for 3 different environments for our project: development, production and test. After that, go to the corresponding config files, located at ~/FinalProject/configs and change the SQLALCHEMY_DATABASE_URI configuration based on this template:
```
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database_name}'
For example: SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@localhost:3306/final_project_development'
```

#### 4. Change the configurations (optional)
Config your SECRET_KEY, JWT_SECRET_KEY, and other configurations based on your favorite cannot be easier. Simply go to ~/FinalProject/configs/base.py and enjoy.

## Starting the server
Run the following command:
```
$ python app.py
```
And the magic will happen on: http://localhost:5000 

## Testing
Simply run the following command:
```
$ pytest --cov=main tests/
```
And a detailed report will be returned.

## Further documentation:
API Docs: (will be updated soon)
