import sqlite3

def open(db_in):
    db_in.type = "SQLite"
    db_in.connection = sqlite3.connect("bot.db3")

def close(db_in):
    db_in.connection.close()

def createTableIfNotExist(db_in, tablename):
    c = db_in.connection.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS ' + tablename + '(id INTEGER PRIMARY KEY);')

def insertToDatabase(db_in, table, dict_in):
    c = db_in.connection.cursor()
    keys = []
    values = []
    for key, value in dict_in.items():
        keys.append(key)
        values.append("'" + value + "'")

    for key in keys:
        try:
            c.execute('ALTER TABLE ' + table.name + ' ADD COLUMN ' + key)
        except:
            pass

    c.execute("INSERT INTO " + table.name + "(" + ",".join(keys) + ") VALUES (" + ",".join(values) + ");")
    db_in.connection.commit()