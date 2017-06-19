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
from api.database.db import DB

def db_open(db_in):
    if DB.type == "SQLite":
        SQLite.db_open(db_in)

def db_close(db_in):
    if DB.type == "SQLite":
        SQLite.close(db_in)

def db_create_table(db_in, tablename):
    if DB.type == "SQLite":
        SQLite.db_create_table(db_in, tablename)

def db_insert(db_in, table, dict_in):
    if DB.type == "SQLite":
        return SQLite.db_insert(db_in, table, dict_in)

def db_get_contents_of_table(db_in, table, rows):
    if DB.type == "SQLite":
        return SQLite.db_get_contents_of_table(db_in, table, rows)