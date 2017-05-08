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
    return plugin.plugin(plugin_in, 'time', [setoffset_command, time_command])

async def onCommand(message_in):
    # Initialize Database

    database.init()
    OffsetTable = table('offsets', tableTypes.pGlobal)
    
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

        # Set Offset in Database

        # Try to update Offset if it exists
        existingOffset = table.search(OffsetTable, 'id', '{}'.format(message_in.author.id))

        if existingOffset != None:
            existingOffset.edit(dict(id=message_in.author.id, offset=normalizedoffset))
        else:
            # Create new entry
            table.insert(OffsetTable, dict(id=message_in.author.id, offset=normalizedoffset))
                # Get time right now
        
        # Return time along with offset
        timeutc = datetime.datetime.utcnow()
        # Apply offset

        if hours > 0:
            # Apply positive offset
            timedelta = datetime.timedelta(hours=hours, minutes=minutes)
            newTime = timeutc + timedelta
        elif hours < 0:
            # Apply negative offset
            timedelta = datetime.timedelta(hours=(-1*hours), minutes=(-1*minutes))
            newTime = timeutc - timedelta
        else:
            # No offset
            newTime = timeutc

        return message.message('Your UTC offset has been set to *{}*, for which time is {}.'.format(normalizedoffset, newTime.strftime("%I:%M %p")))

    
    if message_in.command == 'time':
        memberOrOffset = message_in.body.strip()
        
        # Check whose time we need (or if we got an offset)
        
        if not memberOrOffset:
            member = message_in.author
        else:
            # Try to get a user first
            member = displayname.memberForName(memberOrOffset, message_in.server)
        
        if member:
            existingOffset = table.search(OffsetTable, 'id', '{}'.format(member.id))
            
            # Check if entry exists
            try:
                offset = existingOffset.data[1]
            except Exception:
                return message.message('*{}* didn\'t set an offset. Set an offset with `!setoffset (offset)`.'.format(displayname.name(member)))
        else:
            # Assume input is offset
            offset = memberOrOffset

        offset = offset.replace('+', '')

        # Split time string by : and get hour/minute values
        try:
            hours, minutes = map(int, offset.split(':'))
        except Exception:
            try:
                hours = int(offset)
                minutes = 0
            except Exception:
                return message.message('Invalid offset format. Has to be in +/-HH:MM!')
        
        # Get time right now
        t = datetime.datetime.utcnow()
        # Apply offset

        if hours > 0:
            # Apply positive offset
            offsetmsg += 'UTC+{}'.format(offset)
            td = datetime.timedelta(hours=hours, minutes=minutes)
            newTime = t + td
        elif hours < 0:
            # Apply negative offset
            offsetmsg += 'UTC{}'.format(offset)
            td = datetime.timedelta(hours=(-1*hours), minutes=(-1*minutes))
            newTime = t - td
        else:
            # No offset
            newTime = t

        if member:
            msg = '{}; where *{}* is, it\'s currently *{}*'.format(offsetmsg, displayname.name(member), newTime.strftime("%I:%M %p"))
        else:
            msg = '{} is currently *{}*'.format(offsetmsg, newTime.strftime("%I:%M %p"))
        # Say message
        return message.message(msg)

