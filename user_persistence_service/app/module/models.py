import bcrypt
import uuid
from app import db
from sqlalchemy.dialects.postgresql.base import UUID

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(25), index=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(15), unique=True, index=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = self.generate_password_hash(password)

    def __repr__(self):
        return '<User {}>'.format(self.id)

    # Function for generate password hash
    def generate_password_hash(self, password):
        passwordHash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return passwordHash.decode('utf-8')

    # Function for check whether the password is valid
    def is_valid_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    # Get responsible data
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'username': self.username,
            'password': self.password,
        }
