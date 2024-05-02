# Forum App in Flask Smorest

## Setup the project

- first create virtual environment using pip and activate the virtual env
- then install the necessary package using the command "pip install -r requirements.txt"
- the create the .env file

### In .env file

#### create variable as below:

- DATABASE_USERNAME=your_database_username
- DATABASE_PASSWORD=your_database_password
- DATABASE_HOST=localhost
- DATABASE_PORT=port
- DATABASE_NAME=your_database_name
- JWT_SECRET_KEY=your_secret_key
- JWT_ACCESS_TOKEN_EXPIRES=1
- JWT_REFRESH_TOKEN_EXPIRES=30

## Start the server

- python run.py

## Testing API endpoint

- http://localhost:5000/api/v1/rapidoc
- http://localhost:5000/api/v1/docs
- http://localhost:5000/api/v1/redoc
