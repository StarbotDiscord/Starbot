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

import urllib.parse
from api import command, message, plugin

# Search plugin
def onInit(plugin_in):
    google_command = command.command(plugin_in, 'google', shortdesc='Google it!')
    bing_command = command.command(plugin_in, 'bing', shortdesc='Uhh... Bing it?')
    duckduckgo_command = command.command(plugin_in, 'duckduckgo', shortdesc='Ask the duck.')
    return plugin.plugin(plugin_in, 'search', [google_command, bing_command, duckduckgo_command])

async def onCommand(message_in):
    query = message_in.body.strip()

    # Check if query is nothing
    if not query:
        return message.message('I need a topic to search for!')
    
    # Normalize query
    query = urllib.parse.quote(query)

    # Be kind, don't use lmgtfy/similar
    if message_in.command == 'google':
        msg = "Google search:"
        url = "https://www.google.com/#q="
    if message_in.command == 'bing':
        msg = "Bing search:"
        url = "https://www.bing.com/?q="
    if message_in.command == 'duckduckgo':
        msg = "DuckDuckGo search:"
        url = "https://www.duckduckgo.com/?q="
    
    # Form URL
    url = '{}{}'.format(url,query)

    # Form and return message
    return message.message('{} {}'.format(msg, url))
