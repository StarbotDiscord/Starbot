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
'''Message class and message splitting'''
import textwrap

class message:
    '''Store data about a message.'''
    def __init__(self, body='', file='', embed=None, delete=False, mentions=None, channel=None):
        self.command = None
        self.author = None
        self.server = None
        self.body = body
        self.file = file
        self.embed = embed
        self.delete = delete
        self.mentions = mentions
        self.channel = channel

# Breaks giant message into chunks.
def msg_split(msg, characters: int = 2000):
    '''Split a big message into several smaller ones'''
    if not msg:
        return None

    # Create message list.
    text_list = textwrap.wrap(msg, characters, break_long_words=True, replace_whitespace=False)
    if not text_list:
        return None

    # Create message list objects.
    msg_list = []
    for msg in text_list:
        msg_list.append(message(msg))

    # Return the list.
    return msg_list
