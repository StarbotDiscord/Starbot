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
"""SQLite Abstraction layer for Starbot's database API."""

import sqlite3
from api.database.entry import Entry


def db_open(db_in):
    """Open the Database."""
    db_in.type = "SQLite"
    db_in.connection = sqlite3.connect("bot.db3")


def db_close(db_in):
    """Close the Database."""
    # Close the database.
    db_in.connection.close()


def db_create_table(db_in, tablename):
    """Create a new table in the database unless it already exists."""
    connection = db_in.connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS %s(id INTEGER PRIMARY KEY);' % tablename)


def db_insert(db_in, table, dict_in):
    """Insert new entry in database."""
    connection = db_in.connection.cursor()
    keys = []
    values = []
    for key, value in dict_in.items():
        keys.append(key)
        # Escape quotes
        if isinstance(value, str):
            values.append("'" + value.replace("'", "''") + "'")
        else:
            values.append("'" + str(value) + "'")

    # Update entries for each key and value.
    for key in keys:
        # Attempt to add column, fail silently if it exists.
        try:
            connection.execute('ALTER TABLE %s ADD COLUMN %s' % (table.name, key))
        except sqlite3.OperationalError:
            pass

    connection.execute('INSERT INTO %s(%s) VALUES (%s);' % (table.name, ",".join(keys), ",".join(values)))
    return_entry = Entry(connection.lastrowid, db_in, table, dict_in)
    db_in.connection.commit()
    return return_entry


def db_entry_edit(db_in, table, entry_id, dict_in):
    """Edit existing database entry."""
    connection = db_in.connection.cursor()

    # Update entries for each key and value.
    for key, value in dict_in.items():
        # Attempt to add column, fail silently if it exists.
        try:
            connection.execute('ALTER TABLE %s ADD COLUMN %s' % (table.name, key.replace("'", "''")))
        except sqlite3.OperationalError:
            pass
        # Update the entry in the database.
        connection.execute("UPDATE '%s' SET %s='%s' WHERE id=%s;" % (table.name, key, value, str(entry_id)))

    db_in.connection.commit()


def db_entry_delete(db_in, table, entry_id):
    """Delete database entry."""
    connection = db_in.connection.cursor()
    connection.execute('DELETE FROM %s WHERE id=%s' % (table.name, str(entry_id)))


def db_search(db_in, table, search_key, search_query):
    """Select first entry that matches and return type entry."""
    connection = db_in.connection.cursor()
    search_query = search_query.replace("'", "''")  # Escape quotes
    cursor = connection.execute("SELECT * FROM %s WHERE %s='%s';" %
                                (table.name, search_key, search_query))
    for row in cursor:
        return Entry(row[0], db_in, table, row)

def db_get_contents_of_table(db_in, table, rows):
    connection = db_in.connection.cursor()
    cursor = connection.execute("SELECT %s FROM %s" % (", ".join(rows), table.name))
    results = []
    for row in cursor:
        results.append(row)
    return results
