import glob
import importlib
import time
import sys

import discord
from pluginbase import PluginBase

from api import db, message
from api import command as command_api
from api.bot import bot
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
    bot.plugins.append(plugin_info)

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
        bot.commands.append(command)
        print("Command `{}` registered successfully.".format(command.name))

    # Print success message.
    print("Plugin '{}' registered successfully.".format(plugin_info.name))

class fakeClient:
    def event(self):
        pass

if __name__ == "__main__":
    # Log the time we started.
    bot.startTime = time.time()

    # Get the source of plugins.
    plugin_base = PluginBase(package="plugins")
    plugin_source = plugin_base.make_plugin_source(searchpath=["./plugins"])

    # Load each plugin.
    for plugin in plugin_source.list_plugins():
        initPlugin(plugin)

    # Create the Discord client.
    client = discord.Client()

    # Get our token to use.
    token = ""
    with open("token.txt") as m:
        token = m.read().strip()
else:
    client = discord.Client()


@client.event
async def on_ready():
    # Print logged in message to console.
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")

    # Set the game.
    await client.change_presence(game=discord.Game(name="with magic"))


@client.event
async def on_message(message_in):
    # Ignore messages that aren't from a server and from ourself.
    if message_in.server == None:
        return
    if message_in.author.id == client.user.id:
        return

    isCommand = False

    # Get prefix.
    db.logUserMessage(message_in)
    prefix = db.getPrefix(message_in.server.id)

    # Should we die? Check for exit command.
    if message_in.content == prefix + "exit" or message_in.content == "{} exit".format(message_in.server.me.mention):
        for owner in db.getOwners():
            if str(message_in.author.id) == str(owner):
                sys.exit(0)

    # Check for cache contents command.
    if message_in.content.startswith(prefix + "cachecontents") or message_in.content.startswith("{} cachecontents".format(message_in.server.me.mention)):
        cacheCount = glob.glob("cache/{}_*".format(message_in.content.split(' ')[-1]))
        cacheString = '\n'.join(cacheCount)
        await client.send_message(message_in.channel, "```{}```".format(cacheString))

    # Check each command loaded.
    for command in bot.commands:
        # Do we have a command?
        if command_api.is_command(message_in, prefix, command):
            # Prevent message count increment.
            isCommand = True

            # Send typing message.
            await client.send_typing(message_in.channel)

            # Build message object.
            message_recv = message.message
            message_recv.command = command.name
            if (message_in.content.startswith("{} ".format(message_in.server.me.mention))):
                message_recv.body = message_in.content.split("{} ".format(message_in.server.me.mention) + command.name)[1]
            else:
                message_recv.body = message_in.content.split(prefix + command.name)[1]
            message_recv.author = message_in.author
            message_recv.server = message_in.server
            command_result = command.plugin.onCommand(message_recv)

            # No message, error.
            if command_result == None:
                await client.send_message(message_in.channel,
                                          "**Beep boop - Something went wrong!**\n_Command did not return a result._")

            # Do list of messages, one after the other.
            elif type(command_result) is list:
                for item in command_result:
                    await process_message(message_in, item)

            # Do regular message.
            else:
                await process_message(message_in, command_result)

                # Do we delete the message afterwards?
                if command_result.delete:
                    await client.delete_message(message_in)

    # Increment message counters if not command.
    if not isCommand:
        count = db.getMessageCount(message_in.server.id)
        bot.messagesSinceStart += 1
        count += 1
        db.setMessageCount(message_in.server.id, count)


@client.event
async def on_member_join(member):
    # Welcome new user.
    await client.send_message(member.server, content = "Welcome " + member.mention + " to **" + member.server.name + "**!")

@client.event
async def on_member_remove(member):
    # Say goodbye to user.
    await client.send_message(member.server, content = "Goodbye " + member.mention + ", **" + member.server.name + "** will miss you!")

@client.event
async def on_member_ban(member) :
    # Announce ban.
    await client.send_message(member.server, content = displayname.name(member) + " got banned from **" + member.server.name + "**.")

@client.event
async def on_member_unban(server, user):
    # Announce unban.
    await client.send_message(server, content = displayname.name(user) + " got unbanned from **" + server.name + "**.")


async def process_message(message_in, msg):
    # Remove @everyone and @here from messages.
    if msg.body != "" or msg.embed != None:
        if msg.file != "":
            pass
        elif msg.embed != None:
            if msg.body == "":
                await client.send_message(message_in.channel, embed=msg.embed)
            else:
                zerospace = "​"
                msg.body = msg.body.replace("@everyone", "@{}everyone".format(zerospace)).replace("@here", "@{}here".format(zerospace))
                await client.send_message(message_in.channel, msg.body, embed=msg.embed)
        else:
            zerospace = "​"
            msg.body = msg.body.replace("@everyone", "@{}everyone".format(zerospace)).replace("@here", "@{}here".format(zerospace))
            await client.send_message(message_in.channel, msg.body)
    if msg.file != "":
        if msg.body != "":
            await client.send_file(message_in.channel, msg.file, content=msg.body)
        else:
            await client.send_file(message_in.channel, msg.file)

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
    client.run(token)
