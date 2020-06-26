import config
from app import app, manager

if __name__ == '__main__':
    # Uncomment manager.run() for migrate or update the database model
    # ex: python run.py db migrate
    # manager.run()
    app.run(port=config.PORT, debug=config.DEBUG)
