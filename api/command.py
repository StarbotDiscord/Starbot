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

class Command():
    '''Store information about a command'''
    def __init__(self, plugin, name, shortdesc='no description', devcommand=False):
        self.plugin = plugin
        self.name = name
        self.shortdesc = shortdesc
        self.devcommand = devcommand

def is_command(message_in, prefix, command):
    '''Check if a given message is a command'''

    #First we check if the message starts with our prefix
    if message_in["message"]["content"].startswith(prefix):
        pass

    #Otherwise, the inputted message does not start with a valid bot trigger
    else:
        return False

    # The first part of the message, before the first space
    command_try = message_in["message"]["content"].split(' ')

    # If the first part of the message is equal to the server prefix + the command name
    # This would be used for commands with arguments
    if command_try[0] == prefix + command.name:
        return True

    # If the entire inputted message is equal to a command
    # This will mean the command has no arguments
    elif message_in["message"]["content"] == prefix + command.name:
        return True

    # We have exhausted the possibilities for running a command, so it must not be a command.
    else:
        return False
