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
    c.execute('CREATE TABLE IF NOT EXISTS %s(id INTEGER PRIMARY KEY);' % tablename)

def insertToDatabase(db_in, table, dict_in):
    c = db_in.connection.cursor()
    keys = []
    values = []
    for key, value in dict_in.items():
        keys.append(key)
        values.append("'" + value + "'")

    for key in keys:
        try:
            c.execute('ALTER TABLE %s ADD COLUMN %s' % (table.name, key))
        except:
            pass

    c.execute('INSERT INTO %s(%s) VALUES (%s);' % (table.name, ",".join(keys), ",".join(values)))
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
            c.execute('ALTER TABLE %s ADD COLUMN %s' % (table.name, key))
        except:
            pass
        c.execute("UPDATE '%s' SET %s='%s' WHERE id=%s;" %
                  (table.name, key, value, str(id)))

    db_in.connection.commit()

def deleteEntryInDatabase(db_in, table, id):
    c = db_in.connection.cursor()
    c.execute('DELETE FROM %s WHERE id=%s' % (table.name, str(id)))

def searchInTable(db_in, table, searchTerm, searchFor):
    c = db_in.connection.cursor()
    #cursor = c.execute('SELECT * FROM ' + table.name.replace("'", "''") + ' WHERE ' + searchTerm.replace("'", "''") + '=\'' + searchFor.replace("'", "''") + '\';')
    cursor = c.execute("SELECT * FROM %s WHERE %s='%s';" % (table.name, searchTerm, searchFor))
    for row in cursor:
        print(row[0])
        newEntry = entry(row[0], db_in, table, row)
        return newEntry