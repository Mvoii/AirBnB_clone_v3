#!/usr/bin/python3
"""Creating a flask app"""

import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

# Create a flask app instance
app = Flask(__name__)

# Register blueprint
app.register_blueprint(app_views)

# init cors with app instance
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


# decclare a method for teardown
@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def not_found_page(error):
    """Return a custom 404 error"""
    return ({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    # get env returns a string and port in an int
    # threaded is set ti true to serve multiple requests
    app.run(host=host, port=port, threaded=True)
