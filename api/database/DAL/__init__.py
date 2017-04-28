from api.database.DAL import SQLite
from api.database.db import db

def open(db_in):
    if db.type == "SQLite":
        SQLite.open(db_in)

def close(db_in):
    if db.type == "SQLite":
        SQLite.close(db_in)

def createTableIfNotExist(db_in, tablename):
    if db.type == "SQLite":
        SQLite.createTableIfNotExist(db_in, tablename)

def insertToDatabase(db_in, table, key, value):
    if db.type == "SQLite":
        SQLite.insertToDatabase(db_in, table, key, value)