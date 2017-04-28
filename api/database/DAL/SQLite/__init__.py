import sqlite3

def open(db_in):
    db_in.type = "SQLite"
    db_in.connection = sqlite3.connect("bot.db3")

def close(db_in):
    db_in.connection.close()

def createTableIfNotExist(db_in, tablename):
    c = db_in.connection.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS ' + tablename + '(id INTEGER PRIMARY KEY);')

def insertToDatabase(db_in, table, key, value):
    c = db_in.connection.cursor()
    try:
        c.execute('ALTER TABLE ' + table.name + ' ADD COLUMN ' + key)
    except:
        pass
    print(table.name)
    print(key)
    print(value)
    c.execute("INSERT INTO " + table.name + "(" + key + ") VALUES ('" + value + "');")
    db_in.connection.commit()