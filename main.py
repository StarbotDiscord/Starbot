import glob
import importlib
import time

import discord
import git
from pluginbase import PluginBase

from api import db, message

def initPlugin(plugin, autoImport=True):
    if autoImport == True:
        plugin_temp = plugin_source.load_plugin(plugin)
        plugin_info = plugin_temp.onInit(plugin_temp)
    else:
        plugin_info = plugin.onInit(plugin)
    if plugin_info.plugin == None:
        print("Plugin not defined!")
        pass
    if plugin_info.name == None:
        print("Plugin name not defined")
        pass
    if plugin_info.commands == []:
        print("Plugin did not define any commands.")
        pass
    plugins.append(plugin_info)
    for command in plugin_info.commands:
        if command.plugin == None:
            print("Plugin command does not define parent plugin")
            pass
        if command.name == None:
            print("Plugin command does not define name")
            pass
        commands.append(command)
        print("Command `{}` registered successfully.".format(command.name))
    print("Plugin '{}' registered successfully.".format(plugin_info.name))

class fakeClient:
    def event(self):
        pass

if __name__ == "__main__":
    startTime = time.time()

    plugin_base = PluginBase(package='plugins')
    plugin_source = plugin_base.make_plugin_source(searchpath=['./plugins'])

    plugins = []
    commands = []

    for plugin in plugin_source.list_plugins():
        initPlugin(plugin)

    client = discord.Client()

    token = ''
    with open('token.txt') as m:
        token = m.read().strip()
else:
    client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.change_presence(game=discord.Game(name='with magic'))


@client.event
async def on_message(message_in):
    db.logUserMessage(message_in)
    prefix = db.getPrefix(message_in.server.id)

    if message_in.server == None:
        return

    if message_in.author.id == client.user.id:
        return

    if message_in.content == prefix + 'gitpull':
        if message_in.author.id == "219683089457217536" or message_in.author.id == "186373210495909889":
            pass
        else:
            await client.send_message(message_in.channel, "You do not have permission to git pull.")
        repo = git.Repo(search_parent_directories=True).remotes.origin.pull()
        await client.send_message(message_in.channel, 'Pulled from git.')

    if message_in.content.startswith(prefix + 'reloadplugin'):
        if message_in.author.id == "219683089457217536" or message_in.author.id == "186373210495909889":
            pass
        else:
            await client.send_message(message_in.channel, "You do not have permission to reload plugins.")
        messageSplit = message_in.content.split(' ')
        if len(messageSplit) == 2:

            plugin_base2 = None
            plugin_source2 = None

            plugin_base2 = PluginBase(package='plugins')
            plugin_source2 = plugin_base.make_plugin_source(searchpath=['./plugins'])
            for plugin in plugin_source2.list_plugins():
                plugin_temp = plugin_source2.load_plugin(plugin)
                plugin_info = plugin_temp.onInit(plugin_temp)
                if plugin_info.name == messageSplit[1].strip():
                    for plugin in plugins:
                        if plugin.name == messageSplit[1].strip():
                            importlib.reload(plugin.plugin)
                            await client.send_message(message_in.channel, "Plugin reloaded!")
                            return

            await client.send_message(message_in.channel, "No plugin with that name was found.")
        else:
            await client.send_message(message_in.channel, "Invalid number of args.")

    if message_in.content.startswith(prefix + 'cachecontents'):
        cacheCount = glob.glob('cache/{}_*'.format(message_in.content.split(' ')[-1]))
        cacheString = '\n'.join(cacheCount)
        await client.send_message(message_in.channel, '```{}```'.format(cacheString))
    for command in commands:
        if message_in.content.split(' ')[0] == prefix + command.name or message_in.content == prefix + command.name:
            await client.send_typing(message_in.channel)
            message_recv = message.message
            message_recv.command = command.name
            message_recv.body = message_in.content.split(prefix + command.name)[1]
            message_recv.author = message_in.author
            message_recv.server = message_in.server

            command_result = command.plugin.onCommand(message_recv)

            # No message, error.
            if command_result == None:
                await client.send_message(message_in.channel,
                                          '**Beep boop - Something went wrong!**\n_Command did not return a result._')

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


async def process_message(message_in, msg):
    if msg.body != '' or msg.embed != None:
        if msg.file != '':
            pass
        elif msg.embed != None:
            if msg.body == '':
                await client.send_message(message_in.channel, embed=msg.embed)
            else:
                zerospace = "​"
                msg.body = msg.body.replace("@everyone", "@{}everyone".format(zerospace)).replace("@here",
                                                                                                  "@{}here".format(
                                                                                                      zerospace))
                await client.send_message(message_in.channel, msg.body, embed=msg.embed)
        else:
            zerospace = "​"
            msg.body = msg.body.replace("@everyone", "@{}everyone".format(zerospace)).replace("@here", "@{}here".format(
                zerospace))
            await client.send_message(message_in.channel, msg.body)
    if msg.file != '':
        if msg.body != '':
            await client.send_file(message_in.channel, msg.file, content=msg.body)
        else:
            await client.send_file(message_in.channel, msg.file)

if __name__ == "__main__":
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