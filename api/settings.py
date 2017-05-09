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
    entry_prefix = table.search(table_prefix, 'serverid', '{}'.format(id_server))

    if entry_prefix:
        entry_prefix.edit(dict(serverid=id_server, prefix=prefix))
    else:
        # Create new entry
        table.insert(table_prefix, dict(serverid=id_server, prefix=prefix))


def prefix_get(id_server):
    database.init()
    table_prefix = table('prefixes', tableTypes.pGlobal)
    entry_prefix = table.search(table_prefix, 'serverid', '{}'.format(id_server))

    if entry_prefix:
        return entry_prefix.data[1]
    else:
        return '!'

# Log messages to database.


def message_log(message):
    database.init()
    table_log = table('user_messages', tableTypes.pGlobal)
    table.insert(table_log, dict(userid=message.author.id, username=message.author.name, message=message.content, serverid=message.server.id, servername=message.server.name))

# Manage bot ownership.


def owners_check(id_user):
    database.init()
    table_owners = table('owners', tableTypes.pGlobal)
    entry_owner = table.search(table_owners, 'userid', '{}'.format(id_user))
    if entry_owner:
        return True
    else:
        return False


def owners_get():
    database.init()
    table_owners = table('owners', tableTypes.pGlobal)
    owners = []
    for entry in table_owners:
        owners.append(entry.data[0])
    return owners


def owners_add(id_user):
    database.init()
    table_owners = table('owners', tableTypes.pGlobal)
    entry_owner = table.search(table_owners, 'userid', '{}'.format(id_user))
    if not entry_owner:
        table.insert(table_owners, dict(userid=id_user))

# Manage message log size.


def message_count_set(id_server, count):
    database.init()
    table_message_count = table('messagecounts', tableTypes.pGlobal)
    entry_message_count = table.search(table_message_count, 'serverid', {}.format(id_server))
    if entry_message_count:
        entry_message_count.edit(dict(serverid=id_server, count=count))
    else:
        table.insert(table_message_count, dict(serverid=id_server, count=count))


def message_count_get(id_server):
    database.init()
    table_message_count = table('messagecounts', tableTypes.pGlobal)
    entry_message_count = table.search(table_message_count, 'serverid', {}.format(id_server))
    if entry_message_count:
        return entry_message_count.data[1]
    else:
        return 0
