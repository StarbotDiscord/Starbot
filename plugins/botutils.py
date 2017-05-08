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

import math
import os
import platform
import sys
import time

import discord
import psutil
import pyspeedtest

from api import db, command, message, plugin, git
from api.bot import bot
from libs import progressBar, readableTime, displayname

# Command names.
SERVERSCMD = "servers"
NICKNAMECMD = "nickname"

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
    messages_command   = command.command(plugin_in, 'messages', shortdesc="Show how many messages the bot has seen since start")
    servers_command    = command.command(plugin_in, SERVERSCMD, shortdesc="Show how many servers the bot is on")
    invite_command     = command.command(plugin_in, 'invite', shortdesc="Invite the bot to your server!")
    nickname_command   = command.command(plugin_in, NICKNAMECMD, shortdesc="Change the bot's nickname")
    return plugin.plugin(plugin_in, 'botutils', [plugins_command, commands_command, help_command, info_command, plugintree_command, uptime_command,
                                                 hostinfo_command, cpuinfo_command, setprefix_command, getprefix_command, speedtest_command, addowner_command,
                                                 owners_command, messages_command, servers_command, invite_command, nickname_command])

async def onCommand(message_in):
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
        sha = git.getCommit()
        track = git.getBranch()
        if track == 'master':
            embed = discord.Embed(color=discord.Color.red())
        elif track == 'unstable':
            embed = discord.Embed(color=discord.Color.gold())
        elif track == 'stable':
            embed = discord.Embed(color=discord.Color.green())
        else:
            embed = discord.Embed(color=discord.Color.light_grey())
        embed.set_author(name='Project StarBot v0.2.0-{} on track {}'.format(sha[:7], track), url='https://github.com/1byte2bytes/Starbot/', icon_url='https://pbs.twimg.com/profile_images/616309728688238592/pBeeJQDQ.png')
        embed.add_field(name="Bot Team Alpha", value="CorpNewt\nSydney Erickson\nGoldfish64")
        embed.add_field(name="Source Code", value="Interested in poking around inside the bot?\nClick on the link above!")
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
        # Get information about host environment.
        cpuThread = os.cpu_count()
        cpuUsage = psutil.cpu_percent(interval=1)
        memStats = psutil.virtual_memory()
        memPerc = memStats.percent
        memUsed = memStats.used
        memTotal = memStats.total
        memUsedGB = convert_size(memUsed)
        memTotalGB = convert_size(memTotal)
        currentOS = platform.platform()
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

        # Format hostinfo with OS, CPU, RAM, storage, and other bot info.
        msg = '***{}\'s*** **Home:**\n'.format(displayname.name(message_in.server.me))
        msg += '```Host OS       : {}\n'.format(currentOS)
        msg += 'Host Python   : {}.{}.{} {}\n'.format(pythonMajor, pythonMinor, pythonMicro, pythonRelease)
        if type(cpuThread) != type(1):
            msg += 'Host CPU usage: {}% of {}\n'.format(cpuUsage, platform.machine())
        elif cpuThread > 1:
            msg += 'Host CPU usage: {}% of {} ({} threads)\n'.format(cpuUsage, platform.machine(), cpuThread)
        else:
            msg += 'Host CPU usage: {}% of {} ({} thread)\n'.format(cpuUsage, platform.machine(), cpuThread)
        msg += 'Host RAM      : {} ({}%) of {}\n'.format(memUsedGB, memPerc, memTotalGB)
        msg += 'Host storage  : {} ({}%) of {} - {} free\n'.format(usedStorage, storage.percent, totalStorage, freeStorage)
        msg += 'Hostname      : {}\n'.format(platform.node())
        msg += 'Host uptime   : {}```'.format(readableTime.getReadableTimeBetween(psutil.boot_time(), time.time()))

        # Return completed message.
        return message.message(body=msg)

    if message_in.command == 'cpuinfo':
        # Get CPU usage and create string for message.
        cpuPercents = psutil.cpu_percent(interval=0.1, percpu=True)
        cpuPercentString = '{}\n'.format(platform.processor())

        # First, check to see if we can accurately determine the number of physical cores. If not, omit the core count.
        if psutil.cpu_count(logical=False) == None:
            if psutil.cpu_count() > 1:
                cpuPercentString += '{} threads of {}'.format(psutil.cpu_count(), platform.machine())
            else:
                cpuPercentString += '{} thread of {}'.format(psutil.cpu_count(), platform.machine())
        elif psutil.cpu_count(logical=False) > 1: # Multiple cores.
            cpuPercentString += '{} threads - {} cores of {}'.format(psutil.cpu_count(), psutil.cpu_count(logical=False), platform.machine())
        else:
            if psutil.cpu_count() > 1: # Multiple threads, single core.
                cpuPercentString += '{} threads - {} core of {}'.format(psutil.cpu_count(), psutil.cpu_count(logical=False), platform.machine())
            else: # Single thread, single core.
                cpuPercentString += '{} thread - {} core of {}'.format(psutil.cpu_count(), psutil.cpu_count(logical=False), platform.machine())

        # Build CPU usage graph.
        cpuPercentString += '\n\n'
        for i in range(len(cpuPercents)):
            cpuPercentString += 'CPU {}: {}\n'.format(str(i), progressBar.makeBar(cpuPercents[i]))
        
        # Return completed message.
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

    if message_in.command == "addowner":
        if len(db.getOwners()) != 0:
            try:
                if db.isOwner(message_in.author.id) == True:
                    member = message_in.body.strip()
                    memberCheck = displayname.memberForName(member, message_in.server)

                    if db.isOwner(memberCheck.id):
                        return message.message(body="User is already an owner.")
                    elif memberCheck.bot:
                        return message.message(body="Bots cannot be owners.")
                    else:
                        db.addOwner(memberCheck.id)
                        return message.message(body="Added owner successfully.")
                else:
                    return message.message(body="You aren't an owner of the bot.")
            except Exception as e:
                print(e)
                return message.message(body="Invalid user.")
        else:
            db.addOwner(message_in.author.id)
            return message.message(body="You have successfully claimed yourself as the first owner!")

    if message_in.command == 'owners':
        owners = []
        if len(db.getOwners()) == 0:
            return message.message(body='I have no owners')
        for owner in db.getOwners():
            user = displayname.memberForID(str(owner), message_in.server)
            if user != None:
                owners.append(str(user.name))
            else:
                owners.append(str(owner))
        ownerLst = ', '.join(owners)
        return message.message(body=ownerLst)

    if message_in.command == SERVERSCMD:
        # Get server count.
        servercount = len(bot.client.servers)
        
        # Return message.
        if servercount == 1:
            return message.message("I am a member of **{} server**!".format(servercount))
        else:
            return message.message("I am a member of **{} servers**!".format(servercount))

    if message_in.command == 'messages':
        return message.message("I've witnessed *{} messages* since I started and *{} messages* overall!".format(bot.messagesSinceStart, db.getMessageCount(message_in.server.id)))

    if message_in.command == 'invite':
        return message.message(body=discord.utils.oauth_url(bot.client.user.id, adminPerm))

    if message_in.command == NICKNAMECMD:
        if message_in.channel.permissions_for(message_in.author).manage_nicknames:
            # Change nickname.
            await bot.client.change_nickname(message_in.server.me, message_in.body.strip())
           # if message_in.server.me.nick:
            #    return message.message("My new nickname in this server is **{}**".format(message_in.server.me.nick))
            #else:
             #   return message.message("My nickname has been removed.")
            return message.message("My nickname has been changed.")
        else:
            return message.message("You cannot change nicknames on this server.")

class adminPerm:
    value = 8