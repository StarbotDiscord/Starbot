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
'''Get comics from xkcd.'''

import json
from api import command, caching, message, plugin


def onInit(plugin_in):
    '''List commands for plugin.'''
    xkcd_command = command.Command(plugin_in, 'xkcd', shortdesc='Posts the latest XKCD, or by specific ID')
    return plugin.Plugin(plugin_in, 'comics', [xkcd_command])

async def onCommand(message_in):
    '''Run plugin commands.'''
    if message_in.command == 'xkcd':
        if message_in.body:
            try:
                if int(message_in.body) < 0:
                    return message.Message(body="ID `{}` is not a valid ID".format(message_in.body))
            except ValueError:
                return message.Message(body='Input of `{}` is not a valid number'.format(message_in.body))

            data = json.loads(caching.json_get("https://xkcd.com/{}/info.0.json".format(message_in.body.strip()),
                                              caller='xkcd',
                                              name_custom='{}.json'.format(message_in.body.strip())))
        else:
            data = json.loads(caching.json_get("https://xkcd.com/info.0.json", caller='xkcd', save=False))

        caching.cache_download(data['img'], '{}.png'.format(data['num']), caller='xkcd')

        return message.Message(body='**{}/{}/{} - {}**\n_{}_'.format(data['month'], data['day'], data['year'],
                                                                     data['safe_title'], data['alt']),
                               file='cache/xkcd_{}.png'.format(data['num']))
