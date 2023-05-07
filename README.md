# FalconCRUDApi
This is a containerized application that allows you to perform CRUD operations (Create, Read, Update, Delete) on a set of data using an API built
with Falcon, a Python web framework and TinyDB for persistance.

## Requirements
Docker
## Installation
- Clone this repository to a directory on your local machine
- Open a terminal on the directory the project was cloned in
- Run the following command to build a Docker image of the application:

```docker build -t falcon-crud-api .```

- After the build process is complete, run this command to run the container:

```docker run -p 8000:8000 --name falcon-crud-api falcon-crud-api```

- The API should now be accessible at http://localhost:8000

## Usage

This API has the following endpoints:
- 'GET /users' Retrieve a list of all users
- 'GET /users/{id}' Retrieve a specific user by the ID
- 'POST /users' Create a new user and save to database
- 'PUT /users/{id} Update an existing user
- 'DELETE /users/{id} Delete an existing user
