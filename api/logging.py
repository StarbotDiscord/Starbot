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

# Manage message log size.

from api import database
from api.database.table import table, tableTypes


def message_count_set(id_server, count):
    database.init()
    table_message_count = table('messagecounts', tableTypes.pGlobal)
    try:
        entry_message_count = table.search(table_message_count, 'serverid', '{}'.format(id_server))
    except:
        # TODO: Narrow this and other Exception clauses.
        # Table must be empty.
        entry_message_count = None

    if entry_message_count:
        entry_message_count.edit(dict(serverid=id_server, count=count))
    else:
        table.insert(table_message_count, dict(serverid=id_server, count=count))


def message_count_get(id_server):
    database.init()
    table_message_count = table('messagecounts', tableTypes.pGlobal)
    try:
        entry_message_count = table.search(table_message_count, 'serverid', '{}'.format(id_server))
    except:
        # TODO: Narrow this and other Exception clauses.
        # Table must be empty.
        entry_message_count = None

    if entry_message_count:
        return entry_message_count.data[1]
    else:
        return 0

# Log messages to database.

def message_log(msg):
    database.init()
    table_log = table('user_messages', tableTypes.pGlobal)
    table.insert(table_log, dict(userid=msg.author.id, username=msg.author.name, message=msg.content, serverid=msg.server.id, servername=msg.server.name))

