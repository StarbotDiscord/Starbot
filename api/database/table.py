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

from api.database import DAL
from api.database.db import DB
from api.database.DAL import SQLite

class Table:
    name = None
    table_type = None

    def __init__(self, name_in, type_in):
        self.name = name_in
        self.table_type = type_in

        DAL.db_create_table(DB, self.name)

    def insert(self, dataDict):
        return DAL.db_insert(DB, self, dataDict)

    def search(self, searchTerm, searchFor):
        return SQLite.db_search(DB, self, searchTerm, searchFor)

    def getContents(self, rows):
        return DAL.db_get_contents_of_table(DB, self, rows)

    def getLatestID(self):
        return DAL.db_get_latest_id(DB, self)

class TableTypes:
    pServer = 1
    pGlobal = 2