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

from api import database
from api.database.table import table, tableTypes
# Manage stored prefixes in database.


def prefix_set(id_server, prefix):
    database.init()
    table_prefix = table('prefixes', tableTypes.pGlobal)

    try:
        entry_prefix = table.search(table_prefix, 'serverid', '{}'.format(id_server))
    except:
        # TODO: Narrow this and other Exception clauses.
        # Table must be empty.
        entry_prefix = None

    if entry_prefix:
        entry_prefix.edit(dict(serverid=id_server, prefix=prefix))
    else:
        # Create new entry
        table.insert(table_prefix, dict(serverid=id_server, prefix=prefix))


def prefix_get(id_server):
    database.init()
    table_prefix = table('prefixes', tableTypes.pGlobal)

    try:
        entry_prefix = table.search(table_prefix, 'serverid', '{}'.format(id_server))
    except:
        # TODO: Narrow this and other Exception clauses.
        # Table must be empty.
        entry_prefix = None

    if entry_prefix:
        return entry_prefix.data[1]
    else:
        return '!'


# Manage bot ownership.


def owners_check(id_user):
    database.init()
    table_owners = table('owners', tableTypes.pGlobal)
    try:
        entry_owner = table.search(table_owners, 'userid', '{}'.format(id_user))
    except:
        # TODO: Narrow this and other Exception clauses.
        # Table must be empty.
        entry_owner = None

    if entry_owner:
        return True
    else:
        return False

# TODO: Make tables iterable.

# def owners_get():
#     database.init()
#     table_owners = table('owners', tableTypes.pGlobal)
#     owners = []
#     for entry in table_owners:
#         owners.append(entry.data[0])
#     return owners


def owners_get_old():
    import sqlite3
    conn = sqlite3.connect("bot.db3")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS owners (userid INTEGER)')
    cur = c.execute('SELECT userid FROM owners')
    owners = []
    for row in list(cur):
        owners.append(row[0])
    conn.commit()
    conn.close()
    return owners


def owners_add(id_user):
    database.init()
    table_owners = table('owners', tableTypes.pGlobal)
    try:
        entry_owner = table.search(table_owners, 'userid', '{}'.format(id_user))
    except:
        # TODO: Narrow this and other Exception clauses.
        # Table must be empty.
        entry_owner = None

    if not entry_owner:
        table.insert(table_owners, dict(userid=id_user))

