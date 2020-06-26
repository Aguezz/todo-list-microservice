import config
from .repository import UserRepository
from app import redis_client

class UserCache:
    allow_caching = True if config.CACHING == 'true' else False

    # Init variable data
    def __init__(self):
        self.data = None


    # Function for check if the user is on redis
    def is_exists(self, id):
        # Find the user
        item = redis_client.hgetall('user:{}'.format(id))

        # Return none if is not exists
        return item if item else None


    def set(self, data):
        # Push data to redis
        for k, v in data:
            redis_client.hset('user:{}'.format(data.id), k, v)


    # Function for find a user by id
    def find_by_id(self, id):
        # Check and set data if user is on redis
        self.data = self.is_exists(id)

        # If exists
        if self.data and self.allow_caching:
            return self 

        # If user is not exists, get the data from repository
        user = UserRepository().find_by_id(id)

        # If user doesn't exists in repository
        if not user:
            return None

        # Push data to redis
        for k, v in user.serialize.items():
            redis_client.hset('user:{}'.format(id), k, v)

        return user


    # Function to delete user by id
    def delete_by_id(self, id):
        redis_client.hdel('user:{}'.format(id))


    # Get responsible data
    @property
    def serialize(self):
        # Object data type
        if type(self.data) is dict:
            return {k.decode('utf-8'): v.decode('utf-8') for k, v in self.data.items()}

        return None
