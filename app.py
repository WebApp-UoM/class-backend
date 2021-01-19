from flask import Flask
from flask_jwt_extended import JWTManager
import config, repository
import atexit


def create_app(config_class=config.Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    jwt = JWTManager(app)

    from api import bp
    app.register_blueprint(bp)

    return app

def main():

    app = create_app()
    atexit.register(repository.dbHandler.close)
    app.run(debug=True)


if __name__ == '__main__':
    main()
