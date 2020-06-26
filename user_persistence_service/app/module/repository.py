from app import db, redis_client
from .models import User

class UserRepository:
    # Find a user by id
    def find_by_id(self, id):
        return User.query.filter_by(id=id).first()


    # Find a user by custom field name
    def filter_one(self, query):
        return User.query.filter(query).first()


    def create(self, name, email, username, password):
        user = User(name=name, email=email, username=username, password=password)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            raise e

        return user

    
    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            raise e

        return True


    def delete(self, id):
        user = self.find_by_id(id)
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            raise e

        return True