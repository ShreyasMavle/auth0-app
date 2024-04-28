# Auth0 app for storing & managing users


This Python application connects with the Auth0 database and allows you to create, read, update 
& delete users from the database. This app can be used in CLI as well as on web. 

## API documentation

| HTTP Method | Endpoints                      | Action                                     |
|-------------|--------------------------------|--------------------------------------------|
| GET         | `/users`                       | Get all users in database                  |
| POST        | `/user`                        | Create a new user                          |
| GET         | `/user?email=test@example.com` | Get a specific user using email            |
| PATCH       | `/user`                        | Update user details like email or password |
| DELETE      | `/user?email=test@example.com` | Delete user                                |


## Using it as a CLI app

### Get all users in database:

    python app.py --get-all-users

### Create a new user:
    
    python app.py create-user --email test@example.com --password Test@1234

### Get a specific user using email:

    python app.py get-user --email test@example.com

### Update user details like email or password:

    python app.py update-user --email test@example.com --new-email test1@example.com

    python app.py update-user --email test1@example.com --new_password test1@example.com

### Delete user

    python app.py delete-user --email test1@example.com



