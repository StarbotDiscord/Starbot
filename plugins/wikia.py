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
'''Use the Wikia API to get Definitions'''

from api import command, message, plugin
from api.wikia import Wikia
import discord

import traceback

def wikia_get(wiki, search):
    '''Fetch and return data from Wikia'''
    starwiki = Wikia(wiki)
    try:
        results = starwiki.wikia_search(search)
        page = starwiki.wikia_getpage(results[0]['id'])
        section = page[0]

        resultid = results[0]['id']

        details = starwiki.wikia_getdetails(results[0]['id'])

        # Some really stupid hacks to get the main image
        img_thumb = details[str(resultid)]['thumbnail']
        img_stuff = img_thumb.split("window-crop", 1)
        img_stuff2 = img_stuff[1].split("?")
        img = img_stuff[0][:-1] + "?" + img_stuff2[1]
    except Exception as exc:
        print(exc)
        print(traceback.format_exc())
        return message.Message("No result found for '{}'".format(search))

    if len(section['content']) < 1:
        return message.Message(body="No result found for '{}'".format(search))

    embed = discord.Embed(color=discord.Color.green())
    embed.set_author(name="Visit the full page here",
                     url=results[0]['url'],
                     icon_url='http://slot1.images.wikia.nocookie.net/__cb1493894030/common/skins/common/images/wiki.png')
    embed.add_field(name=section['title'], value=section['content'][0]['text'])
    embed.set_image(url=img)
    return message.Message(embed=embed)

def onInit(plugin_in):
    starwiki_command = command.Command(plugin_in, 'starwiki', shortdesc='Search the Star VS. Wikia')
    wikia_command    = command.Command(plugin_in, 'wikia',    shortdesc='Search Wikia!')
    return plugin.Plugin(plugin_in, 'starwiki', [starwiki_command, wikia_command])

def onCommand(message_in):
    if message_in.command == 'starwiki':
        if message_in.body == '':
            return message.Message(body='Usage:\nstarwiki [search term]')
        else:
            if message_in.body.startswith(" "):
                message_in.body = message_in.body[1:]
            return wikia_get('starvstheforcesofevil', message_in.body)

    if message_in.command == 'wikia':
        if message_in.body == '':
            return message.Message(body='Usage:\nwikia [wikia name] [search term]')

        input_split = message_in.body.split(' ', 2)
        print(input_split)

        if len(input_split) != 3:
            return message.Message(body='Usage:\nwikia [wikia name] [search term]')

        return wikia_get(input_split[1], input_split[2])
