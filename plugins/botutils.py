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

from api import settings, logging, git
from api.bot import Bot
from api.message import Message
from api.command import Command
from api.plugin import Plugin
from libs import progressBar, readableTime, displayname

def commands_detect_dups():
    duplicates = []
    commands_list = []
    for plugin_in in Bot.plugins:
        for command_in in plugin_in.commands:
            commands_list.append(command_in.name)

    for command_in in commands_list:
        commandOccurances = 0
        for command2 in commands_list:
            if command_in == command2:
                commandOccurances += 1
        if commandOccurances > 1:
            duplicates.append(command_in)

    return list(set(duplicates))

def convert_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes/p, 2)
    return '%s %s' % (s, size_name[i])

def onInit(plugin_in: Plugin) -> Plugin:
    plugins_command    = Command(plugin_in, 'plugins',    command_plugins,    shortdesc='Print a list of plugins',                devcommand=True)
    commands_command   = Command(plugin_in, 'commands',   command_commands,   shortdesc='Print a list of commands',               devcommand=True)
    help_command       = Command(plugin_in, 'help',       command_commands,   shortdesc='Print a list of commands')
    info_command       = Command(plugin_in, 'info',       command_info,       shortdesc='Print some basic bot info')
    plugintree_command = Command(plugin_in, 'plugintree', command_plugintree, shortdesc='Print a tree of plugins and commands',   devcommand=True)
    uptime_command     = Command(plugin_in, 'uptime',     command_uptime,     shortdesc='Print the bot\'s uptime',                devcommand=True)
    hostinfo_command   = Command(plugin_in, 'hostinfo',   command_hostinfo,   shortdesc='Prints information about the bots home', devcommand=True)
    cpuinfo_command    = Command(plugin_in, 'cpuinfo',    command_cpuinfo,    shortdesc='Prints info about the system CPUs',      devcommand=True)
    setprefix_command  = Command(plugin_in, 'setprefix',  command_setprefix,  shortdesc='Set the server prefix',                  devcommand=True)
    getprefix_command  = Command(plugin_in, 'getprefix',  command_getprefix,  shortdesc='Get the server prefix',                  devcommand=True)
    speedtest_command  = Command(plugin_in, 'speedtest',  command_speedtest,  shortdesc='Run a speedtest',                        devcommand=True)
    addowner_command   = Command(plugin_in, 'addowner',   command_addowner,   shortdesc='Add a bot owner',                        devcommand=True)
    owners_command     = Command(plugin_in, 'owners',     command_owners,     shortdesc='Print the bot owners',                   devcommand=True)
    return Plugin(plugin_in, 'botutils', [plugins_command, commands_command, help_command, info_command, plugintree_command, uptime_command,
                                                 hostinfo_command, cpuinfo_command, setprefix_command, getprefix_command, speedtest_command, addowner_command,
                                                 owners_command])

async def command_plugins(message_in: Message) -> Message:
    plugin_list = []
    for plugin_in in Bot.plugins:
        plugin_list.append(plugin_in.name)
    return Message(body='```{}```'.format(', '.join(plugin_list)))

async def command_commands(message_in: Message) -> Message:
    cmd_names = []
    cmd_descs = []
    for botcommand in Bot.commands:
        if botcommand.devcommand != True:
            cmd_names.append(botcommand.name)
            cmd_descs.append(botcommand.shortdesc)
    cmd_list = []
    pad_len = len(max(cmd_names, key=len))
    for index, value in enumerate(cmd_names):
        cmd_list.append('{} - {}'.format(cmd_names[index].ljust(pad_len), cmd_descs[index]))
    return Message(body='```{}```'.format('\n'.join(cmd_list)))

async def command_info(message_in: Message) -> Message:
    sha = git.git_commit()
    track = git.git_branch()
    remote = git.get_remote()
    if track == 'master':
        embed = discord.Embed(color=discord.Color.red())
    elif track == 'unstable':
        embed = discord.Embed(color=discord.Color.gold())
    elif track == 'stable':
        embed = discord.Embed(color=discord.Color.green())
    else:
        embed = discord.Embed(color=discord.Color.light_grey())
    embed.set_author(name='Project StarBot v{}-{} on track {}'.format(Bot.version, sha[:7], track))
    embed.set_footer(text="Pulled from {}".format(remote))
    return Message(embed=embed)

async def command_plugintree(message_in: Message) -> Message:
    dups = commands_detect_dups()
    plugin_string = '```\n'
    for plugin_in in Bot.plugins:
        plugin_string += '{}\n'.format(plugin_in.name)
        plugin_commands = len(plugin_in.commands)
        index = 0
        for command_in in plugin_in.commands:
            index += 1
            if plugin_commands != index:
                if command_in.name in dups:
                    plugin_string += '├ {} <-- duplicate\n'.format(command_in.name)
                else:
                    plugin_string += '├ {}\n'.format(command_in.name)
            else:
                if command_in.name in dups:
                    plugin_string += '└ {} <-- duplicate\n'.format(command_in.name)
                else:
                    plugin_string += '└ {}\n'.format(command_in.name)
    plugin_string += '```'
    return Message(body=plugin_string)

async def command_uptime(message_in: Message) -> Message:
    time_current = int(time.time())
    time_str = readableTime.getReadableTimeBetween(Bot.startTime, time_current)
    return Message(body='I\'ve been up for *{}*.'.format(time_str))

async def command_hostinfo(message_in: Message) -> Message:
    # Get information about host environment.
    time_current = int(time.time())

    # CPU stats.
    cpu_threads = os.cpu_count()
    cpu_usage = psutil.cpu_percent(interval=1)

    # Memory stats.
    mem_stats = psutil.virtual_memory()
    mem_percent = mem_stats.percent
    mem_used = convert_size(mem_stats.used)
    mem_total = convert_size(mem_stats.total)

    # Platform info.
    platform_current = platform.platform()

    # Python version info.
    pyver_major = sys.version_info.major
    pyver_minor = sys.version_info.minor
    pyver_micro = sys.version_info.micro
    pyver_release = sys.version_info.releaselevel

    # Storage info.
    stor = psutil.disk_usage('/')
    stor_used = convert_size(stor.used)
    stor_total = convert_size(stor.total)
    stor_free = convert_size(stor.total - stor.used)

    # Format hostinfo with OS, CPU, RAM, storage, and other bot info.
    msg = '***{}\'s*** **Home:**\n'.format(displayname.name(message_in.guild.me))
    msg += '```Host OS       : {}\n'.format(platform_current)
    msg += 'Host Python   : {}.{}.{} {}\n'.format(pyver_major, pyver_minor, pyver_micro, pyver_release)
    if not isinstance(cpu_threads, int):
        msg += 'Host CPU usage: {}% of {}\n'.format(cpu_usage, platform.machine())
    elif cpu_threads > 1:
        msg += 'Host CPU usage: {}% of {} ({} threads)\n'.format(cpu_usage, platform.machine(), cpu_threads)
    else:
        msg += 'Host CPU usage: {}% of {} ({} thread)\n'.format(cpu_usage, platform.machine(), cpu_threads)
    msg += 'Host RAM      : {} ({}%) of {}\n'.format(mem_used, mem_percent, mem_total)
    msg += 'Host storage  : {} ({}%) of {} - {} free\n'.format(stor_used, stor.percent, stor_total, stor_free)
    msg += 'Hostname      : {}\n'.format(platform.node())
    msg += 'Host uptime   : {}```'.format(readableTime.getReadableTimeBetween(psutil.boot_time(), time.time()))

    # Return completed message.
    return Message(body=msg)

async def command_cpuinfo(message_in: Message) -> Message:
    # Get CPU usage and create string for message.
    cpu_pcts = psutil.cpu_percent(interval=0.1, percpu=True)
    cpu_pct_str = '{}\n'.format(platform.processor())
    cpu_threads = psutil.cpu_count()
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_arch = platform.machine()
    # First, check to see if we can accurately determine the number of physical cores. If not, omit the core count.
    if not cpu_cores:
        if cpu_threads > 1:
            cpu_pct_str += '{} threads of {}'.format(cpu_threads, cpu_arch)
        else:
            cpu_pct_str += '{} thread of {}'.format(cpu_threads, cpu_arch)
    elif cpu_cores > 1: # Multiple cores.
        cpu_pct_str += '{} threads - {} cores of {}'.format(cpu_threads, cpu_cores, cpu_arch)
    else:
        if psutil.cpu_count() > 1: # Multiple threads, single core.
            cpu_pct_str += '{} threads - {} core of {}'.format(cpu_threads, cpu_cores, cpu_arch)
        else: # Single thread, single core.
            cpu_pct_str += '{} thread - {} core of {}'.format(cpu_threads, cpu_cores, cpu_arch)

    # Build CPU usage graph.
    cpu_pct_str += '\n\n'
    for index, value in enumerate(cpu_pcts):
        cpu_pct_str += 'CPU {}: {}\n'.format(str(index), progressBar.makeBar(cpu_pcts[index]))

    # Return completed message.
    return Message(body='```{}```'.format(cpu_pct_str))

async def command_setprefix(message_in: Message) -> Message:
    if settings.owners_check(message_in.author.id):
        prefix = message_in.body.split(' ', 1)[-1]
        settings.prefix_set(message_in.guild.id, prefix)
        return Message(body='Prefix set to {}'.format(prefix))
    else:
        return Message(body='Only my owner can set the prefix!')

async def command_getprefix(message_in: Message) -> Message:
    return Message(body='Prefix is {}'.format(settings.prefix_get(message_in.guild.id)))

async def command_speedtest(message_in: Message) -> Message:
    if settings.owners_check(message_in.author.id):
        speed = pyspeedtest.SpeedTest()
        msg = '**Speed Test Results:**\n'
        msg += '```\n'
        msg += '    Ping: {}\n'.format(round(speed.ping(), 2))
        msg += 'Download: {}MB/s\n'.format(round(speed.download()/1024/1024, 2))
        msg += '  Upload: {}MB/s```'.format(round(speed.upload()/1024/1024, 2))
        return Message(body=msg)
    else:
        return Message(body='You do not have permisison to run a speedtest.')

async def command_addowner(message_in: Message) -> Message:
    if settings.owners_get():
        try:
            if settings.owners_check(message_in.author.id):
                member = message_in.body.strip()
                new_member = displayname.memberForName(member, message_in.guild.members, message_in.guild.me)

                if settings.owners_check(new_member.id):
                    return Message(body="User is already an owner.")
                elif new_member.bot:
                    return Message(body="Bots cannot be owners.")
                else:
                    settings.owners_add(new_member.id)
                    return Message(body="Added owner successfully.")
            else:
                return Message(body="You aren't an owner of the bot.")
        except AttributeError:
            return Message(body="Invalid user.")
    else:
        settings.owners_add(message_in.author.id)
        return Message(body="You have successfully claimed yourself as the first owner!")

async def command_owners(message_in: Message) -> Message:
    owners = []
    if not settings.owners_get():
        return Message(body='I have no owners')
    for owner in settings.owners_get():
        user = displayname.memberForID(owner, message_in.guild.members, message_in.guild.me)
        if user:
            owners.append(str(user.name))
        else:
            owners.append(str(owner))
    owner_list = ', '.join(owners)
    return Message(body=owner_list)