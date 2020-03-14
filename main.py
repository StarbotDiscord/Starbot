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

import glob
import importlib
import time
import sys
import asyncio

import discord

from api import settings, message, logging, pluginloader, bot
from api import command as command_api
from api.bot import Bot
from libs import displayname

client = discord.Client()
Bot.client = client


@client.event
async def on_ready():
    # Print logged in message to console.
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    print("Bot Invite Link: " + "https://discordapp.com/oauth2/authorize?client_id=" + str(client.user.id) + "&scope=bot&permissions=8")
    print("------")

    # Set the game.
    await client.change_presence(activity=discord.Game(name="with magic"))


@client.event
async def on_message(message_in):
    # Ignore messages that are from ourselves or another bot
    if message_in.author.id == client.user.id:
        return
    if message_in.author.bot:
        return

    # Get prefix. If not on a server, no prefix is needed.
    #logging.message_log(message_in, message_in.guild.id)
    if message_in.guild:
        prefix = settings.prefix_get(message_in.guild.id)
    else:
        prefix = ""

    # Check each command loaded.
    for command in Bot.commands:
        # Do we have a command?
        if command_api.is_command(message_in, prefix, command):
            # Build message object.
            message_recv = message.Message
            message_recv.command = command.name
            message_recv.body = message_in.content.split(prefix + command.name, 1)[1]
            message_recv.author = message_in.author
            message_recv.guild = message_in.guild
            message_recv.mentions = message_in.mentions
            message_recv.channel = message_in.channel

            command_result = await command.func(message_recv)

            # No message, error.
            if not command_result:
                await message_in.channel.send(
                                        "**Beep boop - Something went wrong!**\n_Command did not return a result._")

            # Do list of messages, one after the other. If the message is more than 5 chunks long, PM it.
            elif type(command_result) is list:
                if len(command_result) > 5:  # PM messages.
                    # Send message saying that we are PMing the messages.
                    await message_in.channel.send(
                                            "Because the output of that command is **{} pages** long, I'm just going to PM the result to you.".format(len(command_result)))

                    # PM it.
                    for item in command_result:
                        await process_message(message_in.author, message_in, item)

                else: # Send to channel.
                    for item in command_result:
                        await process_message(message_in.channel, message_in, item)

            # Do regular message.
            else:
                await process_message(message_in.channel, message_in, command_result)

                # Do we delete the message afterwards?
                if message_in.guild and command_result.delete:
                    await client.delete_message(message_in)

async def process_message(target, message_in, msg):
    # If the message to send has a body
    if msg.body:
        # Remove @everyone and @here from messages.
        zerospace = "​"
        msg.body = msg.body.replace("@everyone", "@{}everyone".format(zerospace)).replace("@here", "@{}here".format(zerospace))

    # If the message to send includes a file
    if msg.file != "":
        # Send the file, along with any possible message
        await target.send(msg.body, embed=msg.embed, file=msg.file)
    else:
        # Send the message, along with a possible embed
        await target.send(msg.body, embed=msg.embed)

if __name__ == "__main__":
    # Init bot variables
    bot.init()

    # Init plugins
    pluginloader.init()

    # Read token
    token = ""
    with open("token.txt") as m:
        token = m.read().strip()

    # Start bot.
    client.run(token)