# Auth0 app for storing & managing users


This Python application connects with the Auth0 database and allows you to create, read, update 
& delete users from the database. It can be used as a CLI or a web app. 

## API documentation

| HTTP Method | Endpoints                      | Action                                           |
|-------------|--------------------------------|--------------------------------------------------|
| GET         | `/users`                       | Get all users in database                        |
| POST        | `/user`                        | Create a new user                                |
| GET         | `/user?email=test@example.com` | Get a specific user using email                  |
| PATCH       | `/user`                        | Update user details like email, password or name |
| DELETE      | `/user?email=test@example.com` | Delete user                                      |


## Using it as a CLI app

### Get all users in database:

    python app.py --get-all-users

### Create a new user:
    
    python app.py create-user --email test@example.com --password Test@1234

### Get a specific user using email:

    python app.py get-user --email test@example.com

### Update user details like email, password or name. Only one field can be changed at a time:

    python app.py update-user --email test@example.com --new-email test1@example.com

    python app.py update-user --email test1@example.com --new-password test1@example.com

    python app.py update-user --email test1@abc.com --new-name TEST1

### Delete user

    python app.py delete-user --email test1@example.com

To get help with CLI commands, use the --help flag

    python app.py --help

## Deployment

Build & run the flask app locally, exposing it on port 8080

    docker build -t auth0-app .
    docker run --name auth0 --rm -p 8080:8080 -it --env-file .env auth0-app

To use it as a CLI app instead, add CLI arguments at the end

    docker run --name auth0 --rm --env-file .env auth0-app --get-all-users
    docker run --name auth0 --rm --env-file .env auth0-app get-user --email test1@test.com


The app is deployed on Google Kubernetes Engine (GKE) cluster in `asia-south1` region. To access it, head over to http://34.93.75.134/

