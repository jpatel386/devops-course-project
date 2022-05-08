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

            

