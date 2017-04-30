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

from api import command, message, plugin, bot


def onInit(plugin_in):
    cachecount_command = command.command(plugin_in, 'cachecount', shortdesc='Count the number of cached items for a command', devcommand=True)
    caches_command =     command.command(plugin_in, 'caches', shortdesc='Count the number of cached items per command', devcommand=True)
    totalcache_command = command.command(plugin_in, 'totalcache', shortdesc='Count the total amount of cached items', devcommand=True)
    return plugin.plugin(plugin_in, 'cacheutils', [cachecount_command, caches_command, totalcache_command])

def onCommand(message_in):
    if message_in.command == 'cachecount':
        if message_in.body == '':
            return message.message(body='No plugin specified')
        return message.message(body='```{}```'.format(len(glob.glob('cache/{}_*'.format(message_in.body.strip())))))

    if message_in.command == 'caches':
        cacheString = ''
        for command in bot.bot.commands:
            commandCacheSize = len(glob.glob('cache/{}_*'.format(command.name)))
            if commandCacheSize > 0:
                cacheString += '{} - {}\n'.format(command.name, commandCacheSize)
        return message.message(body='```{}```'.format(cacheString))

    if message_in.command == 'totalcache':
        return message.message(body='```{}```'.format(len(glob.glob('cache/*'))))