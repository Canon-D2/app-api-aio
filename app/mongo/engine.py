from .config import *
from motor.motor_asyncio import AsyncIOMotorClient


class Engine(object):
    def __init__(self, database_name: str) -> None:
        database_url = f'mongodb://mgdb/{database_name}?retryWrites=true&w=majority'
        # database_url = f"mongodb://localhost/{database_name}"
        database_driver = AsyncIOMotorClient(database_url)
        self.driver = database_driver[database_name]

    def get_database(self):
        return self.driver
    
    def __new__(cls, database_name: str):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Engine, cls).__new__(cls)
        return cls.instance
    
    
engine_aio = Engine(AIO_DATABASE_NAME).get_database()
engine_logs = Engine(LOGS_DATABASE_NAME).get_database()
engine_tracking = Engine(TRACKING_DATABASE_NAME).get_database()