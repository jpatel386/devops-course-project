import os


class Config:
    """Base configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions? .env file not found. Please create from template")

    trello_key = os.environ.get('trello_key')
    if not trello_key:
        raise ValueError("No trello_key defined for flask app. Please set this in .env")
    trello_token = os.environ.get('trello_token')
    if not trello_token:
        raise ValueError("No trello_token defined for flask app. Please set this in .env")
    trello_board_id = os.environ.get('trello_board_id')
    if not trello_board_id:
        raise ValueError("No trello_board_id defined for flask app. Please set this in .env")