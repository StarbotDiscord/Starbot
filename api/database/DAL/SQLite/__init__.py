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