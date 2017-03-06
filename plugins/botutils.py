import plugin
import command
import message
import main

import git

def onInit(plugin_in):
    plugins_command = command.command(plugin_in, 'plugins')
    commands_command = command.command(plugin_in, 'commands')
    help_command = command.command(plugin_in, 'help')
    info_command = command.command(plugin_in, 'info')
    return plugin.plugin(plugin_in, 'botutils', [plugins_command, commands_command, help_command, info_command])

def onCommand(message_in):
    if message_in.command == 'plugins':
        pluginList = []
        for plugin in main.plugins:
            pluginList.append(plugin.name)
        return message.create(body='```{}```'.format(', '.join(pluginList)))
    if message_in.command == 'commands' or message_in.command == 'help':
        commandList = []
        for command in main.commands:
            commandList.append(command.name)
        return message.create(body='```{}```'.format(', '.join(commandList)))
    if message_in.command == 'info':
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        return message.create(body='```Project StarBot v0.0.1-{}\nDeveloped by CorpNewt and Sydney Erickson```'.format(sha[:7]))