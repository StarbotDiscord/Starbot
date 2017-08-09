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

from api import command, message, plugin, caching
import urllib
import json
import discord

def onInit(plugin_in):
    wikipedia_command = command.Command(plugin_in, 'wikipedia', shortdesc='Search Wikipedia, The Free Encyclopedia')
    return plugin.Plugin(plugin_in, 'wikipedia', [wikipedia_command])

async def onCommand(message_in):
    searchstring = urllib.parse.quote(str.title(message_in.body.strip()))
    if not searchstring:
        return message.Message("Usage: `!wikipedia [article name]")
    # Form URL

    formatargs = '?format=json&formatversion=2'
    actionarg = 'query'
    propargs = '&prop=extracts&exintro=&explaintext='
    otherargs = '&redirects=1'

    url = 'https://en.wikipedia.org/w/api.php{}&action={}{}{}&titles={}'
    url = url.format(formatargs, actionarg, propargs, otherargs, searchstring)

    wikidata_json = caching.json_get(url, caller='wikipedia', name_custom=searchstring)
    wikidata = json.loads(wikidata_json)

    try:
        missing = wikidata["query"]["pages"][0]["missing"]
    except KeyError:
        missing = False
    if missing:
        return message.Message("Article {} doesn't exist on Wikipedia!".format(searchstring))

    title = wikidata["query"]["pages"][0]["title"]
    extract = wikidata["query"]["pages"][0]["extract"]

    # Cleanly cut extract to 900 characters

    if len(extract) >= 900:
        extract = extract[:900]
        extract = extract.rsplit('\n', 1)[0] # Cut to nearest paragraph.
        extract = extract.rsplit('.', 1)[0] + '.' # Cut to nearest sentence.

    # Form Embed card

    embed = discord.Embed(color=discord.Color.green())
    embed.set_author(name=title)
    embed.add_field(name='From Wikipedia, The free Encyclopedia', value=extract)

    return message.Message(embed=embed)
