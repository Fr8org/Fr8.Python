"""
This script runs the terminalTwitter application using a development server.
"""

from os import environ
from terminalTwitter.main import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '38080'))
    except ValueError:
        PORT = 38080
    app.run(HOST, PORT)
