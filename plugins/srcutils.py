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

def onInit(plugin_in):
    gitsrc_command = command.Command(plugin_in, 'source', shortdesc='Get the git repo for the bot!')
    docs_command = command.Command(plugin_in, 'docs', shortdesc='Get a link to the bot\'s documentation')
    tests_command = command.Command(plugin_in, 'tests', shortdesc='Get a link to the bot\'s tests')
    return plugin.Plugin(plugin_in, 'tinyurl', [gitsrc_command, docs_command, tests_command])

def onCommand(message_in):
    if message_in.command == 'source':
        return message.Message(body="https://github.com/StarbotDiscord/Starbot")
    if message_in.command == 'docs':
        return message.Message(body="http://starbot.readthedocs.io/en/latest/")
    if message_in.command == 'tests':
        return message.Message(body="https://travis-ci.org/StarbotDiscord/Starbot")