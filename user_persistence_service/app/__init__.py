import config
import redis
import sys
from flask import Flask, jsonify
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

# Configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_POSTGRES_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

# Redis configuration
# redis_client = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
redis_client = redis.Redis.from_url(config.REDIS_URI)

# Check redis connection
if config.CACHING == 'true':
    try:
        redis_client.ping()
    except Exception as e:
        print(e)
        print('Something wrong with redis connection')
        sys.exit(0)

# Initialization
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

# Check postgres connection
try:
    db.session.execute("SELECT 1")
except Exception as e:
    print(e)
    print('Something wrong with postgres connection')
    sys.exit(0)

# Add to command
# Ex: python3 app.py db init, migrate, upgrade
manager.add_command('db', MigrateCommand)

# Register blueprint
from app.module.controllers import module
app.register_blueprint(module)

# Handle endpoint not found
@app.errorhandler(404)
def not_found(error ):
    return jsonify(success=False, message='Endpoint not found.', data=None), 404
