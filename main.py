import discord
import asyncio
import git
import message
from pluginbase import PluginBase

plugin_base = PluginBase(package='plugins')
plugin_source = plugin_base.make_plugin_source(searchpath=['./plugins'])

plugins = []
commands = []

for plugin in plugin_source.list_plugins():
    plugin_temp = plugin_source.load_plugin(plugin)
    plugin_info = plugin_temp.onInit(plugin_temp)
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

for command in commands:
    print(command.plugin)
    print(command.name)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message_in):
    if message_in.content.startswith('!info'):
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        await client.send_message(message_in.channel, '```Project StarBot v0.0.1-{}\r\nDeveloped by CorpNewt and Sydney Erickson```'.format(sha[:5]))
    for command in commands:
        if message_in.content.split(' ')[0] == '!' + command.name or message_in.content == '!' + command.name:
            await client.send_typing(message_in.channel)
            message_recv = message.message
            message_recv.command = command.name
            message_recv.body = message_in.content.split('!' + command.name)[-1]

            command_result = command.plugin.onCommand(message_recv)

            if command_result == None:
                await client.send_message(message_in.channel, '**INTERNAL BOT ERROR**\nCommand did not return a result.')

            if command_result.body != None:
                await client.send_message(message_in.channel, command_result.body)
            if command_result.file != None:
                await client.send_file(message_in.channel, command_result.file)

token = ''
with open('token.txt') as m:
    token = m.read().strip()

client.run(token)