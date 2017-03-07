import plugin
import command
import message
import main
import time

from libs import readableTime
import git

def detectDuplicateCommands():
    duplicates = []
    commandsL = []
    for plugin in main.plugins:
        for command in plugin.commands:
            commandsL.append(command.name)

    for command in commandsL:
        commandOccurances = 0
        for command2 in commandsL:
            if command == command2:
                commandOccurances += 1
        if commandOccurances > 1:
            duplicates.append(command)

    return list(set(duplicates))

def onInit(plugin_in):
    plugins_command = command.command(plugin_in, 'plugins')
    commands_command = command.command(plugin_in, 'commands')
    help_command = command.command(plugin_in, 'help')
    info_command = command.command(plugin_in, 'info')
    plugintree_command = command.command(plugin_in, 'plugintree')
    uptime_command = command.command(plugin_in, 'uptime')
    return plugin.plugin(plugin_in, 'botutils', [plugins_command, commands_command, help_command, info_command, plugintree_command, uptime_command])

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

    if message_in.command == 'plugintree':
        dups = detectDuplicateCommands()
        pluginString = '```\n'
        for plugin in main.plugins:
            pluginString += '{}\n'.format(plugin.name)
            commandsInPlugin = len(plugin.commands)
            currentCommand = 0
            for command in plugin.commands:
                currentCommand += 1
                if commandsInPlugin != currentCommand:
                    if command.name in dups:
                        pluginString += '├ {} <-- duplicate\n'.format(command.name)
                    else:
                        pluginString += '├ {}\n'.format(command.name)
                else:
                    if command.name in dups:
                        pluginString += '└ {} <-- duplicate\n'.format(command.name)
                    else:
                        pluginString += '└ {}\n'.format(command.name)
        pluginString += '```'
        return message.create(body=pluginString)

    if message_in.command == 'uptime':
        currentTime = int(time.time())
        timeString = readableTime.getReadableTimeBetween(main.startTime, currentTime)
        return message.create(body='I\'ve been up for *{}*.'.format(timeString))