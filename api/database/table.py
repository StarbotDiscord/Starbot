from api.database import DAL
from api.database.db import db

class table:
    name = None
    table_type = None

    def __init__(self, name_in, type_in):
        self.name = name_in
        self.table_type = type_in

        DAL.createTableIfNotExist(db, self.name)

    def insert(self, dataDict):
        for key, value in dataDict.items():
            DAL.insertToDatabase(db, self, key, value)

class tableTypes:
    pServer = 1
    pGlobal = 2