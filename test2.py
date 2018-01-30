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

import glob
import importlib
import time
import sys
import asyncio

import syddiscord
from pluginbase import PluginBase

from api import settings, message, logging
from api import command as command_api
from api.bot import Bot
from libs import displayname

def initPlugin(plugin, autoImport=True):
    # Init plugin.
    if autoImport == True:
        plugin_temp = plugin_source.load_plugin(plugin)
        plugin_info = plugin_temp.onInit(plugin_temp)
    else:
        plugin_info = plugin.onInit(plugin)

    # Verify the plugin is defined, it has a name, and it has commands.
    if plugin_info.plugin == None:
        print("Plugin not defined!")
        pass
    if plugin_info.name == None:
        print("Plugin name not defined")
        pass
    if plugin_info.commands == []:
        print("Plugin did not define any commands.")
        pass

    # Add plugin to list.
    Bot.plugins.append(plugin_info)

    # Load each command in plugin.
    for command in plugin_info.commands:
        # Verify command has a parent plugin and a name.
        if command.plugin == None:
            print("Plugin command does not define parent plugin")
            pass
        if command.name == None:
            print("Plugin command does not define name")
            pass

        # Add command to list of commands and print a success message.
        Bot.commands.append(command)
        print("Command `{}` registered successfully.".format(command.name))

    # Print success message.
    print("Plugin '{}' registered successfully.".format(plugin_info.name))

class FakeClient:
    def event(self):
        pass

if __name__ == "__main__":
    from api import database
    database.init()

    # Log the time we started.
    Bot.startTime = time.time()

    # Get the source of plugins.
    plugin_base = PluginBase(package="plugins")
    plugin_source = plugin_base.make_plugin_source(searchpath=["./plugins"])

    # Load each plugin.
    for plugin in plugin_source.list_plugins():
        initPlugin(plugin)

    # Get our token to use.
    token = ""
    with open("token.txt") as m:
        token = m.read().strip()

async def on_ready():
    # Print logged in message to console.
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    print("Bot Invite Link: " + "https://discordapp.com/oauth2/authorize?client_id=" + client.user.id + "&scope=bot&permissions=8")
    print("------")

    # Set the game.
    client.change_presence(game=discord.Game(name="with magic"))

def on_message(message_in):
    # Ignore messages that aren't from a server and from ourself.
    #if not message_in.server:
     #   return
    print(message_in["myself"])
    if message_in["message"]["author"]["id"] == message_in["myself"]["id"]:
        return

    is_command = False

    # Get prefix. If not on a server, no prefix is needed.
    #logging.message_log(message_in, message_in.server.id)
    prefix = settings.prefix_get(message_in["guild"]["id"])


    # Should we die? Check for exit command.
    if message_in["message"]["content"] == prefix + "exit":
        if settings.owners_check(message_in["message"]["author"]["id"]):
            sys.exit(0)

    # Check for cache contents command.
    if message_in["message"]["content"].startswith(prefix + "cachecontents"):
        cacheCount = glob.glob("cache/{}_*".format(message_in["message"]["content"].split(' ')[-1]))
        cacheString = '\n'.join(cacheCount)
        syddiscord.send_message(message_in["channel"]["id"], "```{}```".format(cacheString))

    # Check each command loaded.
    for command in Bot.commands:
        # Do we have a command?
        if command_api.is_command(message_in, prefix, command):
            # Prevent message count increment.
            is_command = True

            # Send typing message.
            # syddiscord.send_typing(message_in["channel"]["id"])

            # Build message object.
            message_recv = message.Message
            message_recv.command = command.name
            message_recv.body = message_in["message"]["content"].split(prefix + command.name, 1)[1]
            message_recv.author = message_in["message"]["author"]
            message_recv.server = message_in["guild"]
            message_recv.mentions = message_in["message"]["mentions"]
            message_recv.channel = message_in["channel"]

            command_result = command.plugin.onCommand(message_recv)

            # No message, error.
            if not command_result:
                client.send_message(message_in.channel,
                                          "**Beep boop - Something went wrong!**\n_Command did not return a result._")

            # Do list of messages, one after the other. If the message is more than 5 chunks long, PM it.
            elif type(command_result) is list:
                if len(command_result) > 5:  # PM messages.
                    # Send message saying that we are PMing the messages.
                    client.send_message(message_in.channel,
                                              "Because the output of that command is **{} pages** long, I'm just going to PM the result to you.".format(len(command_result)))

                    # PM it.
                    for item in command_result:
                        process_message(message_in.author, message_in, item)

                else: # Send to channel.
                    for item in command_result:
                        process_message(message_in.channel, message_in, item)

            # Do regular message.
            else:
                process_message(message_in["channel"]["id"], message_in, command_result)

    # Increment message counters if not command.
    if message_in["guild"] and not is_command:
        logging.message_log(message_in, message_in["guild"]["id"])
        count = logging.message_count_get(message_in["guild"]["id"])
        Bot.messagesSinceStart += 1
        count += 1

def process_message(target, message_in, msg):
    # If the message to send has a body
    if msg.body:
        # Remove @everyone and @here from messages.
        zerospace = "​"
        msg.body = msg.body.replace("@everyone", "@{}everyone".format(zerospace)).replace("@here", "@{}here".format(zerospace))

    # If the message to send includes a file
    if msg.file != "":
        # Send the file, along with any possible message
        client.send_file(target, msg.file, content=msg.body)
    else:
        # Send the message, along with a possible embed
        #client.send_message(target, msg.body, embed=msg.embed)
        syddiscord.send_message(target, msg.body)

if __name__ == "__main__":
    # Start bot.
    # THIS MUST ALWAYS BE DOWN HERE
    # I found this out after 3 days of stupidity and tried filing a report with the Discord.py devs to figure out why the
    # library seems to have hanged when it was in the initial block of the same if. I still don't know. They disregarded
    # the entirety of my ticket and told me that this is a blocking call. Yeah, I know. But if you read the rest of the ticket
    # you would know that after this function was called all the main thread would drop and the bot would become unresponsive.
    # But apparently it is the debugger I explicitly stated that I had turned off on some of my messages I sent while figuring it out.
    # I don't know why you would lock a ticket because of a debugger that isn't on and a problem you were ignoring.
    # Maybe someone should add a warning to the Discord.py library for when you run client.run in the wrong place.
    # But honestly I can't be bothered.
    syddiscord.new_message_func = on_message
    syddiscord.connect(token)
