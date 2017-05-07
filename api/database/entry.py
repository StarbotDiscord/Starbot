from api.database.DAL import SQLite

class entry:
    id = None
    db = None
    table = None
    data = None

    def __init__(self, input_id, database, table_in, data):
        self.id = input_id
        self.db = database
        self.table = table_in

    def edit(self, newData):
        SQLite.editInDatabase(self.db, self.table, self.id, newData)

    def delete(self):
        SQLite.deleteEntryInDatabase(self.db, self.table, self.id)