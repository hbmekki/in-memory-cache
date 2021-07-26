from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from instance.config import config
from .cache import EvictionStrategies, Cache
from .api import CacheApi


def create_app(config_name):
    """Creates and configures an instance of the flask app.

    This method allows the creation of instances of the application with
    different configurations. It is useful specially for testing.

    input:
        config_name: the name of the configuartion to use.
    """

    # instantiate an app where config will be in an instance
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    cor_app = CORS(app)

    # Set the config parameters
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py')
    
    # Initialize the cache using the config params
    cache = Cache(
        app.config['NUMBER_OF_SLOTS'], 
        app.config['TIME_TO_LIVE'], 
        EvictionStrategies(app.config['EVICTION_POLICY'])
    )
    CacheApi.initialize_cache(cache)

    # Set the routes
    
    api.add_resource(CacheApi, '/object/<string:key>')

    return app