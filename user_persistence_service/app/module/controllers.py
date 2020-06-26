from .models import User
from .cache import UserCache
from .repository import UserRepository
from app import db, redis_client
from app.libs import response
from flask import Blueprint, request, jsonify
from sqlalchemy import and_, or_

module = Blueprint('module', __name__)

# Create user route
@module.route('/', methods=['POST'])
def store():
    # Initialize variable
    name = email = username = password = None

    # Get the data & trim them
    try:
        name = request.json['name'].strip()
        email = request.json['email'].strip()
        username = request.json['username'].strip()
        password = request.json['password']

    except Exception as e:
        print(e)
        print('store() Error while get data from request')
        return response.fail(message=response.MISSING_FIELD), 400

    # Find the current user where using this username or email
    # other_user = User.query.filter((User.username == username) | (User.email == email)).first()
    other_user = UserRepository().filter_one((User.username == username) | (User.email == email))

    # Check whether the current user's email or username same with the input username
    if other_user:
        if other_user.email == email:
            return response.fail(message='Email already exists.'), 400

        return response.fail(message='Username already exists.'), 400

    try:
        # Create new user
        user = UserRepository().create(name=name, email=email, username=username, password=password)
    except Exception as e:
        print(e)
        print('store() Error while create new user')
        return response.fail(message=response.INTERNAL_SERVER_ERROR), 500

    return response.success(data=user.serialize), 201


# Find one user route
@module.route('/<uuid:id>', methods=['GET'])
def findOne(id):
    # Find a user by id
    user = UserCache().find_by_id(id)

    # If user exists
    if user:
        return response.success(data=user.serialize), 200

    # If user doesn't exists
    return response.fail(message=response.RECORD_NOT_FOUND), 404


# Update user route
@module.route('/<uuid:id>', methods=['PATCH'])
def update(id):
    # Find a user by id
    user = UserRepository().find_by_id(id)

    # Check if user doesn't exists
    if not user:
        return response.fail(message=response.RECORD_NOT_FOUND), 404

    # Initialize variable
    name = email = username = None

    # Get the data & trim them
    try:
        name = request.json['name'].strip()
        email = request.json['email'].strip()
        username = request.json['username'].strip()
    except Exception as e:
        print(e)
        print('update() Error while get data from request')
        return response.fail(message=response.MISSING_FIELD), 400

    # Check whether other users are using the same email or username
    other_user = UserRepository().filter_one(and_(User.id != id, or_(User.email == email, User.username == username)))

    # If other users with this email or password is exists
    if other_user:
        if other_user.email == email:
            return response.fail(message='Email already exists.'), 400
        if other_user.username == username:
            return response.fail(message='Username already exists.'), 400

    # Set old data with new data
    user.name = name
    user.email = email
    user.username = username

    # Update user
    try:
        UserRepository().update()
    except Exception as e:
        print(e)
        print('update() error while updating data.')
        return response.fail(message=response.INTERNAL_SERVER_ERROR), 500

    return response.success(message=response.UPDATED_SUCCESSFULLY, data=user.serialize), 200


# Delete user route
@module.route('/<uuid:id>', methods=['DELETE'])
def delete(id):
    # Get current user by id and delete
    user = UserCache().find_by_id(id)

    # Check if user exists
    if user:
        try:
            # Delete the user
            UserRepository().delete(id)

            # Also delete the cache
            UserCache().delete_by_id(id)
        except Exception as e:
            print(e)
            print('delete() Error while delete the user.')
            return response.fail(message=response.INTERNAL_SERVER_ERROR), 500

        return response.success(message=response.DELETED_SUCCESSFULLY), 200

    # If user doesn't exists, return 404 not found
    return response.fail(message=response.RECORD_NOT_FOUND), 404


# Change password route
@module.route('/<uuid:id>/change_password', methods=['PATCH'])
def change_password(id):
    # Find a user
    user = UserRepository().find_by_id(id)

    # If user doesn't exists
    if not user:
        return jsonify(success=False, message='Record not found.', data=None), 404

    # Initialization variable
    old_password = new_password = None

    # Get the data
    try:
        old_password = request.json['old_password']
        new_password = request.json['new_password']
    except Exception as e:
        print(e)
        print('change_password() Error while get the data')
        return response.fail(message=response.INTERNAL_SERVER_ERROR), 500

    # Check whether the current password match
    is_valid_password = user.is_valid_password(old_password)

    # If the current password not match
    if not is_valid_password:
        return response.fail(message='Wrong password.'), 400

    # Set new password
    # It's very important
    user.password = user.generate_password_hash(new_password)

    # Update user's password
    try:
        UserRepository().update()
    except Exception as e:
        print(e)
        print('change_password() error while updating user\'s password.')
        return response.fail(message=response.INTERNAL_SERVER_ERROR), 500

    return response.success(message=response.UPDATED_SUCCESSFULLY), 200


# Delete all caching
'''Uncomment next function if you want to delete all cache'''
# @module.route('/redis/delete_all', methods=['GET'])
# def redis_delete_all():
#     redis_client.flushall()
#     return 'success'
