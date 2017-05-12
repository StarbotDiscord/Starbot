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
'''Get cache usage info'''

import glob
from api import command, message, plugin, bot


def onInit(plugin_in):
    '''List commands for plugin.'''
    desc_base = 'Count the number of cached items '
    desc_cachecount = desc_base + 'for a command'
    desc_caches = desc_base + 'per command'
    desc_totalcache = desc_base + 'stored'
    cachecount_command = command.command(plugin_in, 'cachecount', shortdesc=desc_cachecount, devcommand=True)
    caches_command = command.command(plugin_in, 'caches', shortdesc=desc_caches, devcommand=True)
    totalcache_command = command.command(plugin_in, 'totalcache', shortdesc=desc_totalcache, devcommand=True)
    return plugin.plugin(plugin_in, 'cacheutils', [cachecount_command, caches_command, totalcache_command])

async def onCommand(message_in):
    '''Run plugin commands.'''
    if message_in.command == 'cachecount':
        if message_in.body == '':
            return message.message(body='No plugin specified')
        return message.message(body='```{}```'.format(len(glob.glob('cache/{}_*'.format(message_in.body.strip())))))

    if message_in.command == 'caches':
        cache_str = ''
        for cmd in bot.bot.commands:
            cmd_cache_size = len(glob.glob('cache/{}_*'.format(cmd.name)))
            if cmd_cache_size > 0:
                cache_str += '{} - {}\n'.format(cmd.name, cmd_cache_size)
        return message.message(body='```{}```'.format(cache_str))

    if message_in.command == 'totalcache':
        return message.message(body='```{}```'.format(len(glob.glob('cache/*'))))
