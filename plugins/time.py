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

import datetime
from api import command, message, plugin, database
from api.database.table import table, tableTypes
from api.database.entry import entry
from libs import displayname

def onInit(plugin_in):
    # Set Commands
    setoffset_command = command.command(plugin_in, 'setoffset', shortdesc='Set your UTC offset.')
    time_command = command.command(plugin_in, 'time', shortdesc='Get local time.')
    return plugin.plugin(plugin_in, 'time', [setoffset_command])

async def onCommand(message_in):
    if message_in.command == 'setoffset':
        # Normalize offset
        offsetstr = message_in.body.strip()
        
        if offsetstr[0] == '+':
            prefix = '+'
        else:
            prefix = ''
        
        try:
            hours, minutes = map(int, offsetstr.split(':'))
        except Exception:
            try:
                hours = int(offsetstr)
                minutes = 0
            except Exception:
                return message.message('Incorrect Offset format. Has to be in +/-HH:MM!')
        normalizedoffset = '{}{}:{}'.format(prefix, hours, minutes)

        # Set Offset
        database.init()
        OffsetTable = table('offsets', tableTypes.pGlobal)

        existingOffset = table.search(OffsetTable, 'id', '{}'.format(message_in.author.id))
        print(existingOffset)
        if existingOffset != None:
            OffsetEntry = entry(message_in.author.id, database, 'offsets', dict(offset=existingOffset[2]))
            OffsetEntry.delete()

        table.insert(OffsetTable, dict(id=message_in.author.id, offset=normalizedoffset))
        
        return message.message('Your UTC offset has been set to *{}!*'.format(normalizedoffset))


#    if message_in.command == 'time':

        # Check whose time we need