import os
import requests

# Where the server is running
PORT = os.environ.get('PORT', 8081)

# Debugging while running only in a development environment
DEBUG = False if os.environ.get('PYTHON_ENV') == 'production' else True

# Get configurations from centralized configuration service
CENTRALIZED_CONFIGURATION_SERVICE = os.environ.get('CENTRALIZED_CONFIGURATION_SERVICE', 'http://localhost:8080')
config = requests.get(CENTRALIZED_CONFIGURATION_SERVICE).json()

# Postgres URI database
SQLALCHEMY_POSTGRES_URI = config['USER_PERSISTENCE_SERVICE_POSTGRES_URI']
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Redis configuration
CACHING = os.environ.get('CACHING', 'true')
REDIS_URI = config['USER_PERSISTENCE_SERVICE_REDIS_URI']
