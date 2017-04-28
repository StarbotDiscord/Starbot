from api.database import DAL
from api.database.db import db

class table:
    def __init__(self, name, type):
        name = None
        type = None

        DAL.createTableIfNotExist(db, name)

    def insert(self, dataDict):
        pass

class tableTypes:
    pServer = 1
    pGlobal = 2