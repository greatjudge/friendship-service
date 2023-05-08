# friendship-service
## Introduction

This is the Implementation of a test assignment for an internship in VK. This backend is built using the Django web framework, and uses Django REST framework to provide a RESTful API for the friendship actions. Users can send, reject applications to friends, delete from friends, view lists of friends and applications.

## Requirements

To run this backend, you will need to have the following installed on your system:

   * Python
   * Django
   * Django REST framework
   * Postgres

## Installation
1. Clone the repository.
2. Navigate to the project directory: `cd friendship-service`.
3. Create a virtual environment: `python3 -m venv env`.
4. Activate the virtual environment: `source env/bin/activate`.
5. Install the dependencies: `python -m pip install -r requirements.txt`.
6. Dont remember to set django secter key. You can create the file .env in the same folder with manage.py and write to it `DJANGO_SECRET_KEY`="...(this key)...". There is example of .env file: `example_.env`.
8. Run the database migrations: `python manage.py migrate`.

Or you can use `docker-compose.yml`

## Run server
To start the server, run the following command: `python manage.py runserver`.  
The server will start running at `http://localhost:8000/`.

## Usage Examples
After starting server you can make requests to it.
