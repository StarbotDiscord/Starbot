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

from api import command, message, plugin

# Search plugin
def onInit(plugin_in):
    google_command = command.command(plugin_in, 'google', shortdesc='Google it!')
    bing_command = command.command(plugin_in, 'bing', shortdesc='Uhh... Bing it?')
    duckduckgo_command = command.command(plugin_in, 'duckduckgo', shortdesc='Ask the duck.')
    return plugin.plugin(plugin_in, 'fun', [google_command, bing_command, duckduckgo_command])

def onCommand(message_in):
    query = message_in.body.strip()

    # Check if query is nothing
    if query == None:
        return message.message('I need a topic to search for!')
    
    # Be kind, don't use lmgtfy/similar
    if message_in.command == 'google':
        msg = "Google search: https://www.google.com/?q="
    if message_in.command == 'bing':
        msg = "Bing search: https://www.bing.com/?q="
    if message_in.command == 'tableflip':
        msg = "DuckDuckGo search: https://www.duckduckgo.com/?q="
    
    # Form and return message
    return message.message('{}{}'.format(msg, quote(query))
