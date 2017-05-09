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


#import api.wikia
#starwiki = api.wikia.Wikia('starvstheforcesofevil')
#results = starwiki.search('Star Butterfly')
#print(results)
#print(results[0]['id'])
#print(starwiki.getPage(results[0]['id'])[0]['title'])

from api import command, message, plugin
from api.wikia import Wikia
import discord

def onInit(plugin_in):
    tinyurl_command = command.command(plugin_in, 'starwiki', shortdesc='Search the Star VS. Wikia')
    return plugin.plugin(plugin_in, 'starwiki', [tinyurl_command])

async def onCommand(message_in):
    if message_in.body == '':
        return message.message(body='Usage:\nstarwiki [search term]')
    else:
        starwiki = Wikia('starvstheforcesofevil')
        results = starwiki.search(message_in.body)
        page = starwiki.getPage(results[0]['id'])
        section = page[0]

        if len(section['content']) < 1:
            return message.message(body="No result found for '{}'".format(message_in.body))

        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name="Visit the full page here",
                         url=results[0]['url'],
                         icon_url='http://slot1.images.wikia.nocookie.net/__cb1493894030/common/skins/common/images/wiki.png')
        embed.add_field(name=section['title'], value=section['content'][0]['text'])
        return message.message(embed=embed)