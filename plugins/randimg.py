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

import random
import urllib.error
import urllib.request

from api import command, caching, message, plugin


def onInit(plugin_in):
    goldfish_command = command.command(plugin_in, 'goldfish', shortdesc='Post a random picture of a goldfish to the channel')
    return plugin.plugin(plugin_in, 'randimg', [goldfish_command])

async def onCommand(message_in):
    # Goldfish
    if message_in.command == 'goldfish':
        try:
            f = urllib.request.urlopen("http://goldfishapi.azurewebsites.net/goldfish/rand.php").read().decode("utf-8")
        except urllib.error.URLError as e:
            return message.message(body='There was an issue connecting to goldfish API.'.format(message_in.body))

        imageName = f.split('/')
        caching.cache_download(f, imageName[-1], caller='goldfish')

        return message.message(file='cache/goldfish_' + imageName[-1])
