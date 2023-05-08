# friendship-service
## Introduction

This is the Implementation of a test assignment for an internship in VK. This backend is built using the Django web framework, and uses Django REST framework to provide a RESTful API for the friendship actions. Users can send, reject applications to friends, delete from friends, view lists of friends and applications.

## Installation
1. Clone the repository.
2. Navigate to the project directory: `cd friendship-service`.
3. Create `.env` file in friendship directory (file in the same folder with manage.py) with the contents like in example_.env.  
If you want use sqlite you can just remove the lines startswith "DB_". Dont forget about secret_key
4.  Create `.env` file in friendship-service with the contents like in example_.env.db

#### without docker
3. Create a virtual environment: `python3 -m venv env`.
4. Activate the virtual environment: `source env/bin/activate`.
5. Install the dependencies: `python -m pip install -r requirements.txt`.
6. Dont remember to set django secter key. You can create the file .env in the same folder with manage.py and write to it `DJANGO_SECRET_KEY`="...(this key)...". There is example of .env file: `example_.env`.
7. Run the database migrations: `python manage.py migrate`.

## Run server
#### using manage.py.
1. To start the server, run the following command: `python manage.py runserver`.  
2. The server will start running at `http://localhost:8000/`.

#### using `Dockerfile`.
1. Build image: `docker build -t friendship:1.0 .`
2. Run conrainer and server on 127.0.0.1:8000: `docker run -it --rm -p 127.0.0.1:8000:8000 friendship:1.0`.  
--rm delete container after stop and it is not necessary.
3. The server will start running at `http://localhost:8000/`.

#### using docker compose.
1. run command `docker compose up`
2. The server will start running at `http://friendship.localhost`.

## Usage Examples
After starting server you can make requests to it.

#### 1. Registration.
```commandline
POST /users/register/

Headers:
Content-Type: application/json

Request Body:
{
    "username": "unique_username",
    "password": "password123",
    "password2": "password123"
}
```

#### 2. Get all friends.
```commandline
GET /friends/

Headers:
Authorization: Basic <base64_encoded_credentials>
```

#### 3. Get friendship with user_id 4.
```commandline
GET /friends/4

Headers:
Authorization: Basic <base64_encoded_credentials>
```

#### 4. Delete friend with id 4.
```commandline
DELETE /friends/4

Headers:
Authorization: Basic <base64_encoded_credentials>
```

#### 5. Get incoming and outgoing requests.
```commandline
GET /friends/friend_requests/

Headers:
Authorization: Basic <base64_encoded_credentials>
```

#### 6. Send friend request to user with id 4
```commandline
POST /users/register/

Headers:
Content-Type: application/json
Authorization: Basic <base64_encoded_credentials>

Request Body:
{
    "user_to": 4
}
```

#### 7. Get friend request to user 4.
```commandline
GET /friends/friend_requests/4/

Headers:
Authorization: Basic <base64_encoded_credentials>
```

#### 8. DELETE friend request to user with id 4
```commandline
DELETE /friends/friend_requests/4/

Headers:
Authorization: Basic <base64_encoded_credentials>
```

#### 9. Accept friend request from user with id 4
```commandline
POST /friends/friend_requests/accepter/4/

Headers:
Authorization: Basic <base64_encoded_credentials>
```

#### 10. Reject friend request from user with id 4
```commandline
PATCH /friends/friend_requests/accepter/4/

Headers:
Authorization: Basic <base64_encoded_credentials>
```

#### 11. Delete friend request from user with id 4
```commandline
DELETE /friends/friend_requests/accepter/4/

Headers:
Authorization: Basic <base64_encoded_credentials>
```
