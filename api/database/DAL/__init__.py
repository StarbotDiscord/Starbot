from api.database.DAL import SQLite
from api.database.db import db

def open(db_in):
    if db.type == "SQLite":
        SQLite.open(db_in)