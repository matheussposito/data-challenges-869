# pylint: disable=missing-docstring

import os

def start():
    """returns the right message"""
    if os.environ.get('FLASK_ENV', 'Starting in production mode...') == 'development':
        return 'Starting in development mode...'
    return 'Starting in production mode...'

if __name__ == "__main__":
    print(start())
