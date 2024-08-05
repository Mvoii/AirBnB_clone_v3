#!/usr/bin/python3
"""Creating a flask app"""

import os
from flask import Flask
from models import storage
from api.v1.views import app_views

# Create a flask app instance
app = Flask(__name__)

# Register blueprint
app.register_blueprint(app_views)


# decclare a method for teardown
@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    # get env returns a string and port in an int
    # threaded is set ti true to serve multiple requests
    app.run(host=host, port=port, threaded=True)
