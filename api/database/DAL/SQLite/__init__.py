#    Copyright 2017 Starbot Discord Project
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import sqlite3
from api.database.entry import entry

def open(db_in):
    db_in.type = "SQLite"
    db_in.connection = sqlite3.connect("bot.db3")

def close(db_in):
    db_in.connection.close()

def createTableIfNotExist(db_in, tablename):
    c = db_in.connection.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS ' + tablename.replace("'", "\\'") + '(id INTEGER PRIMARY KEY);')

def insertToDatabase(db_in, table, dict_in):
    c = db_in.connection.cursor()
    keys = []
    values = []
    for key, value in dict_in.items():
        keys.append(key.replace("'", "\\'"))
        values.append("'" + value.replace("'", "\\'") + "'")

    for key in keys:
        try:
            c.execute('ALTER TABLE ' + table.name + ' ADD COLUMN ' + key)
        except:
            pass

    c.execute("INSERT INTO " + table.name.replace("'", "\\'") + "(" + ",".join(keys) + ") VALUES (" + ",".join(values) + ");")
    return_entry = entry(c.lastrowid, db_in, table, dict_in)
    db_in.connection.commit()
    return return_entry

def editInDatabase(db_in, table, id, dict_in):
    c = db_in.connection.cursor()
    keys = []
    values = []
    tableArray = []
    for key, value in dict_in.items():
        try:
            c.execute('ALTER TABLE ' + table.name.replace("'", "\\'") + ' ADD COLUMN ' + key.replace("'", "\\'"))
        except:
            pass
        print("UPDATE " + table.name.replace("'", "\\'") + " SET " + key.replace("'", "\\'") + "=" + value.replace("'", "\\'") + " WHERE id=" + str(id).replace("'", "\\'") + ";")
        c.execute("UPDATE " + table.name.replace("'", "\\'") + " SET " + key.replace("'", "\\'") + "='" + value.replace("'", "\\'") + "' WHERE id=" + str(id).replace("'", "\\'") + ";")

    db_in.connection.commit()

def deleteEntryInDatabase(db_in, table, id):
    c = db_in.connection.cursor()
    c.execute('DELETE FROM ' + table.name.replace("'", "\\'") + ' WHERE id=' + str(id).replace("'", "\\'"))

def searchInTable(db_in, table, searchTerm, searchFor):
    c = db_in.connection.cursor()
    cursor = c.execute('SELECT * FROM ' + table.name.replace("'", "\\'") + ' WHERE ' + searchTerm.replace("'", "\\'") + '=\'' + searchFor.replace("'", "\\'") + '\';')
    for row in cursor:
        print(row[0])
        newEntry = entry(row[0], db_in, table, row)
        return newEntry