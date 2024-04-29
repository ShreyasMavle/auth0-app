import argparse
import os
import requests
import json
from flask import Flask, request, jsonify
import sys

app = Flask(__name__)

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUDIENCE = os.getenv("AUDIENCE")

headers = {
    'content-type': 'application/json'
}


# Common functions for CLI & API
def get_access_token():
    url = f'https://{AUTH0_DOMAIN}/oauth/token'

    payload = {
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET,
        'audience': AUDIENCE,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None


def create_user(email, password):
    url = f'https://{AUTH0_DOMAIN}/api/v2/users'
    headers['Authorization'] = f'Bearer {get_access_token()}'

    payload = {
        'email': email,
        'password': password,
        'connection': 'Username-Password-Authentication'
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 201:
        return {'message': 'User created successfully'}, 201
    error_message = response.json().get("message", 'Failed to create user')
    return {'error': error_message}, response.status_code


def get_user_by_email(email):
    url = f'https://{AUTH0_DOMAIN}/api/v2/users'
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }
    params = {'q': f'email:"{email}"'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        users = response.json()
        if users:
            # Assuming there's only one user with this email
            return users[0], 200
        else:
            return [], 200
    error_message = response.json().get("message", 'User not found')
    return {'message': error_message}, response.status_code


def get_all_users():
    url = f'https://{AUTH0_DOMAIN}/api/v2/users'
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        users = response.json()
        return users, 200
    else:
        error_message = response.json().get("message", 'Failed to fetch users')
        return {'error': error_message}, response.status_code


def update_user_by_email(email, new_email=None, new_password=None):
    user = get_user_by_email(email)
    if user[0] and user[1] == 200:
        url = f"https://{AUTH0_DOMAIN}/api/v2/users/{user[0]['user_id']}"
        headers['Authorization'] = f'Bearer {get_access_token()}'

        payload = {}
        if new_email:
            payload['email'] = new_email
        elif new_password:
            payload['password'] = new_password
        response = requests.patch(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            return {'message': 'User updated successfully'}, 200
        else:
            error_message = response.json().get("message", "Failed to update user")
            return {'error': error_message}, response.status_code
    else:
        return user


def delete_user_by_email(email):
    user = get_user_by_email(email)
    if user[0] and user[1] == 200:
        url = f"https://{AUTH0_DOMAIN}/api/v2/users/{user[0]['user_id']}"
        headers = {
            'Authorization': f'Bearer {get_access_token()}'
        }
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'error': 'Failed to delete user'}, response.status_code
    else:
        return user


# Flask API routes
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "routes": [
            "GET  /users, Get all users in database",
            "POST  /user, Create a new user",
            "GET  /user?email=test@example.com, Get a specific user using email",
            "PATCH  /user, Update user details like email or password",
            "DELETE  /user?email=test@example.com, Delete user"
        ]
    }), 200


@app.route('/user', methods=['POST'])
def create_user_route():
    data = request.get_json()
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400
    result, status_code = create_user(data['email'], data['password'])
    return jsonify(result), status_code


@app.route('/users', methods=['GET'])
def get_all_users_route():
    users, status_code = get_all_users()
    return jsonify(users), status_code


@app.route('/user', methods=['GET'])
def get_user_route():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    result, status_code = get_user_by_email(email)
    if not result:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(result), status_code


@app.route('/user', methods=['PATCH'])
def update_user_route():
    data = request.get_json()
    email = data.get('email')
    new_email = data.get('new_email')
    new_password = data.get('new_password')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    result, status_code = update_user_by_email(email, new_email, new_password)
    if not result:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(result), status_code


@app.route('/user', methods=['DELETE'])
def delete_user_route():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    result, status_code = delete_user_by_email(email)
    if not result:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(result), status_code


def cli():
    parser = argparse.ArgumentParser(description='Auth0 User Management CLI')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    create_parser = subparsers.add_parser('create-user', help='Create a user')
    create_parser.add_argument('--email', help='Email address of the user')
    create_parser.add_argument('--password', help='Password of the user')

    get_parser = subparsers.add_parser('get-user', help='Get a user by email')
    get_parser.add_argument('--email', help='Email address of the user')

    update_parser = subparsers.add_parser('update-user', help='Update a user by email')
    update_parser.add_argument('--email', help='Email address of the user')
    update_parser.add_argument('--new-email', help='New email address of the user. Enter only one field to '
                                                   'be updated at a time')
    update_parser.add_argument('--new-password', help='New password of the user. Enter only one field to '
                                                      'be updated at a time')

    delete_parser = subparsers.add_parser('delete-user', help='Delete a user by email')
    delete_parser.add_argument('--email', help='Email address of the user')

    parser.add_argument('--get-all-users', action='store_true', dest='get_all_users', help='Get all users')

    args = parser.parse_args()

    result = ""
    if args.get_all_users:
        result, _ = get_all_users()
    elif args.command == 'create-user':
        result, _ = create_user(args.email, args.password)
    elif args.command == 'get-user':
        result, _ = get_user_by_email(args.email)
    elif args.command == 'update-user':
        result, _ = update_user_by_email(args.email, args.new_email, args.new_password)
    elif args.command == 'delete-user':
        result, _ = delete_user_by_email(args.email)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    # if command line arguments are present, use it as CLI app
    if len(sys.argv) > 1:
        cli()
    else:
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
