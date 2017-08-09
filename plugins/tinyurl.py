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

from urllib.request import urlopen
import urllib

from api import command, message, plugin


def onInit(plugin_in):
    tinyurl_command = command.Command(plugin_in, 'tinyurl', shortdesc='Convert a link to a TinyURL')
    return plugin.Plugin(plugin_in, 'tinyurl', [tinyurl_command])

async def onCommand(message_in):
    if message_in.body == '':
        return message.Message(body='Usage:\ntinyurl [url]')
    else:
        try:
            urllib.request.urlopen(message_in.body.strip())
            return message.Message(body=urlopen("http://tinyurl.com/api-create.php?url=" + message_in.body.strip()).read().decode("utf-8"))
        except Exception as e:
            return message.Message(body='That website doesn\'t seem to exist')