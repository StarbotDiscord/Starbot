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

def insertToDatabase(db_in, table, dict_in):
    if db.type == "SQLite":
        SQLite.insertToDatabase(db_in, table, dict_in)