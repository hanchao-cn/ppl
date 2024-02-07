import logging
import os

from quart import Quart

from . import server  # noqa


def create_app():
    if not os.getenv("RUNNING_IN_PRODUCTION"):
        logging.basicConfig(level=logging.DEBUG)

    app = Quart(__name__,instance_relative_config=True)
    
    app.register_blueprint(server.bp)

    return app
