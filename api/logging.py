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
from api.database.table import Table, TableTypes


def message_count_get(server_id):
    '''Get the current message count.'''
    database.init()
    table_message_count = Table('user_messages_{}'.format(server_id), TableTypes.pGlobal)
    return table_message_count.getLatestID()

# Log messages to database.

def message_log(msg, server_id):
    '''Log a message into the database.'''
    database.init()
    table_log = Table('user_messages_{}'.format(server_id), TableTypes.pGlobal)
    Table.insert(table_log, dict(userid=msg.author.id, username=msg.author.name,
                                 message=msg.content, serverid=msg.server.id,
                                 servername=msg.server.name))
