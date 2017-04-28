import sqlite3

def open(db_in):
    db_in.type = "SQLite"
    db_in.connection = sqlite3.connect("bot.db3")

def createTableIfNotExist(db_in, tablename):
    c = db_in.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS {} ()'.format(tablename))