import os


class Config:
    """Base configuration variables."""
    
    def __init__(self):
        self.mongo_db_connection = os.environ.get('mongo_db_connection')
        if not self.mongo_db_connection:
            raise ValueError("No mongo_db_connection set. Please set this in the .env file as per the instructions.")

        self.mongo_db_name = os.environ.get('mongo_db_name')
        if not self.mongo_db_name:
            raise ValueError("No mongo_db_name set. Please set this in the .env file as per the instructions.")

        self.git_client_id = os.environ.get('git_client_id')
        if not self.git_client_id:
            raise ValueError("No git_client_id set. Please set this in the .env file as per the instructions.")
        
        self.git_client_secret = os.environ.get('git_client_secret')
        if not self.git_client_secret:
            raise ValueError("No git_client_secret set. Please set this in the .env file as per the instructions.")

        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY set. Please set this in the .env file as per the instructions.")
        
        # Not needed unless doing tests and so we don't need to verify if there is a value or not
        self.LOGIN_DISABLED = os.getenv('LOGIN_DISABLED') == 'True'

        self.LOG_LEVEL = os.getenv('LOG_LEVEL') == 'DEBUG'
        
        self.LOGGLY_TOKEN = os.getenv('LOGGLY_TOKEN')
        

            

