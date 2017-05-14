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

from api import command, message, plugin, database
from api.bot import Bot
from api.database.table import Table, TableTypes
from libs import displayname

# Command names.
SETWELCOMECMD = "setwelcome"

def onInit(plugin_in):
    setwelcome_command = command.Command(plugin_in, SETWELCOMECMD, shortdesc="Set the welcome message for the server.")
    return plugin.Plugin(plugin_in, "greetings", [setwelcome_command])

@Bot.client.event
async def on_member_join(member):
    # Welcome new user.
    await Bot.client.send_message(member.server, content = "Welcome " + member.mention + " to **" + member.server.name + "**!")

@Bot.client.event
async def on_member_remove(member):
    # Say goodbye to user.
    await Bot.client.send_message(member.server, content = "Goodbye " + member.mention + ", **" + member.server.name + "** will miss you!")

@Bot.client.event
async def on_member_ban(member) :
    # Announce ban.
    await Bot.client.send_message(member.server, content = displayname.name(member) + " got banned from **" + member.server.name + "**.")

@Bot.client.event
async def on_member_unban(server, user):
    # Announce unban.
    await Bot.client.send_message(server, content = displayname.name(user) + " got unbanned from **" + server.name + "**.")


async def onCommand(message_in):
    # Initialize database.
    database.init()
    table_greetings = Table("greetings", TableTypes.pServer)


