import math
import os
import platform
import sys
import time

import discord
import git
import psutil
import pyspeedtest

import main
from api import db, command, message, plugin
from api.bot import bot
from libs import progressBar
from libs import readableTime


def detectDuplicateCommands():
    duplicates = []
    commandsL = []
    for plugin in bot.plugins:
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

def convert_size(size_bytes):
   if (size_bytes == 0):
       return '0B'
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes/p, 2)
   return '%s %s' % (s, size_name[i])

def onInit(plugin_in):
    plugins_command    = command.command(plugin_in, 'plugins', shortdesc='Print a list of plugins', devcommand=True)
    commands_command   = command.command(plugin_in, 'commands', shortdesc='Print a list of commands')
    help_command       = command.command(plugin_in, 'help', shortdesc='Redirects to !commands')
    info_command       = command.command(plugin_in, 'info', shortdesc='Print some basic bot info')
    plugintree_command = command.command(plugin_in, 'plugintree', shortdesc='Print a tree of plugins and commands', devcommand=True)
    uptime_command     = command.command(plugin_in, 'uptime', shortdesc='Print the bot\'s uptime', devcommand=True)
    hostinfo_command   = command.command(plugin_in, 'hostinfo', shortdesc='Prints information about the bots home', devcommand=True)
    cpuinfo_command    = command.command(plugin_in, 'cpuinfo', shortdesc='Prints info about the system CPUs', devcommand=True)
    setprefix_command  = command.command(plugin_in, 'setprefix', shortdesc='Set the server prefix', devcommand=True)
    getprefix_command  = command.command(plugin_in, 'getprefix', shortdesc='Get the server prefix', devcommand=True)
    speedtest_command  = command.command(plugin_in, 'speedtest', shortdesc='Run a speedtest', devcommand=True)
    addowner_command   = command.command(plugin_in, 'addowner', shortdesc='Add a bot owner', devcommand=True)
    owners_command     = command.command(plugin_in, 'owners', shortdesc='Print the bot owners', devcommand=True)
    return plugin.plugin(plugin_in, 'botutils', [plugins_command, commands_command, help_command, info_command, plugintree_command, uptime_command,
                                                 hostinfo_command, cpuinfo_command, setprefix_command, getprefix_command, speedtest_command, addowner_command, owners_command])

def onCommand(message_in):
    if message_in.command == 'plugins':
        pluginList = []
        for plugin in bot.plugins:
            pluginList.append(plugin.name)
        return message.message(body='```{}```'.format(', '.join(pluginList)))

    if message_in.command == 'commands' or message_in.command == 'help':
        commandNames = []
        commandDescs = []
        for command in bot.commands:
            if command.devcommand != True:
                commandNames.append(command.name)
                commandDescs.append(command.shortdesc)
        commandList = []
        padLength = len(max(commandNames, key=len))
        for i in range(len(commandNames)):
            commandList.append('{} - {}'.format(commandNames[i].ljust(padLength), commandDescs[i]))
        return message.message(body='```{}```'.format('\n'.join(commandList)))

    if message_in.command == 'info':
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        track = repo.active_branch.name
        if track == 'master':
            embed = discord.Embed(color=discord.Color.red())
        elif track == 'unstable':
            embed = discord.Embed(color=discord.Color.gold())
        elif track == 'stable':
            embed = discord.Embed(color=discord.Color.green())
        else:
            embed = discord.Embed(color=discord.Color.light_grey())
        embed.set_author(name='Project StarBot v0.1.2-{} on track {}'.format(sha[:7], track), url='https://github.com/1byte2bytes/Starbot/', icon_url='https://pbs.twimg.com/profile_images/616309728688238592/pBeeJQDQ.png')
        embed.set_footer(text='Created by CorpNewt and Sydney Erickson')
        return message.message(embed=embed)

    if message_in.command == 'plugintree':
        dups = detectDuplicateCommands()
        pluginString = '```\n'
        for plugin in bot.plugins:
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
        return message.message(body=pluginString)

    if message_in.command == 'uptime':
        currentTime = int(time.time())
        timeString = readableTime.getReadableTimeBetween(bot.startTime, currentTime)
        return message.message(body='I\'ve been up for *{}*.'.format(timeString))

    if message_in.command == 'hostinfo':
        cpuThred = os.cpu_count()
        cpuUsage = psutil.cpu_percent(interval=1)
        memStats = psutil.virtual_memory()
        memPerc = memStats.percent
        memUsed = memStats.used
        memTotal = memStats.total
        memUsedGB = "{0:.1f}".format(((memUsed / 1024) / 1024) / 1024)
        memTotalGB = "{0:.1f}".format(((memTotal / 1024) / 1024) / 1024)
        currentOS = platform.platform()
        system = platform.system()
        release = platform.release()
        version = platform.version()
        currentTime = int(time.time())
        pythonMajor = sys.version_info.major
        pythonMinor = sys.version_info.minor
        pythonMicro = sys.version_info.micro
        pythonRelease = sys.version_info.releaselevel
        storage = psutil.disk_usage('/')
        usedStorage = convert_size(storage.used)
        totalStorage = convert_size(storage.total)
        freeStorage = convert_size(storage.total - storage.used)

        msg = '***{}\'s*** **Home:**\n'.format('StarBot')
        msg += '```Host OS       : {}\n'.format(currentOS)
        msg += 'Host Python   : {}.{}.{} {}\n'.format(pythonMajor, pythonMinor, pythonMicro, pythonRelease)
        if cpuThred > 1:
            msg += 'Host CPU usage: {}% of {} ({} threads)\n'.format(cpuUsage, platform.machine(), cpuThred)
        else:
            msg += 'Host CPU usage: {}% of {} ({} thread)\n'.format(cpuUsage, platform.machine(), cpuThred)
        msg += 'Host RAM      : {}GB ({}%) of {}GB\n'.format(memUsedGB, memPerc, memTotalGB)
        msg += 'Host HDD      : {} ({}%) of {} - {} free\n'.format(usedStorage, storage.percent, totalStorage, freeStorage)
        msg += 'Hostname      : {}\n'.format(platform.node())
        msg += 'Host uptime   : {}```'.format(readableTime.getReadableTimeBetween(psutil.boot_time(), time.time()))

        return message.message(body=msg)

    if message_in.command == 'cpuinfo':
        cpuPercents = psutil.cpu_percent(interval=0.1, percpu=True)
        cpuPercentString = '{}\n'.format(platform.processor())
        if psutil.cpu_count(logical=False) > 1:
            cpuPercentString += '{} threads - {} cores'.format(psutil.cpu_count(), psutil.cpu_count(logical=False))
        else:
            if psutil.cpu_count() > 1:
                cpuPercentString += '{} threads - {} core'.format(psutil.cpu_count(), psutil.cpu_count(logical=False))
            else:
                cpuPercentString += '{} thread - {} core'.format(psutil.cpu_count(), psutil.cpu_count(logical=False))
        cpuPercentString += '\n\n'
        for i in range(len(cpuPercents)):
            cpuPercentString += 'CPU {}: {}\n'.format(str(i), progressBar.makeBar(cpuPercents[i]))
        return message.message(body='```{}```'.format(cpuPercentString))

    if message_in.command == 'setprefix':
        if message_in.author.id == '219683089457217536':
            prefix = message_in.body.split(' ', 1)[-1]
            db.setPrefix(message_in.server.id, prefix)
            return message.message(body='Prefix set to {}'.format(prefix))

    if message_in.command == 'getprefix':
        if message_in.author.id == '219683089457217536':
            return message.message(body='Prefix is {}'.format(db.getPrefix(message_in.server.id)))

    if message_in.command == 'speedtest':
        if db.isOwner(message_in.author.id) == True:
            st = pyspeedtest.SpeedTest()
            msg = '**Speed Test Results:**\n'
            msg += '```\n'
            msg += '    Ping: {}\n'.format(round(st.ping(), 2))
            msg += 'Download: {}MB/s\n'.format(round(st.download()/1024/1024, 2))
            msg += '  Upload: {}MB/s```'.format(round(st.upload()/1024/1024, 2))
            return message.message(body=msg)
        else:
            return message.message(body='You do not have permisison to run a speedtest.')

    if message_in.command == 'addowner':
        if len(db.getOwners()) != 0:
            try:
                if db.isOwner(message_in.author.id) == True:
                    temp = message_in.body.split('<@')
                    uid = temp[-1][:-1]
                    int(uid)
                    db.addOwner(uid)
                    return message.message(body='Added owner successfully')
                else:
                    return message.message(body='You aren\'t an owner of the bot')
            except Exception as e:
                return message.message(body='Invalid user')
        else:
            db.addOwner(message_in.author.id)
            return message.message(body='You have successfully claimed yourself as the first owner!')

    if message_in.command == 'owners':
        owners = []
        for owner in db.getOwners():
            print(owner)
            user = main.client.get_user_info(owner)
            owners.append(user.name)
        print(owners)
        ownerLst = ', '.join(owners)
        return message.message(body=ownerLst)
