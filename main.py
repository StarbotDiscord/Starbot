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
from pluginbase import PluginBase

from api import settings, message, logging, bot
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
    # Ignore messages that aren't from a server and from ourself.
    #if not message_in.guild:
     #   return
    if message_in.author.id == client.user.id:
        return
    if message_in.author.bot:
        return

    is_command = False

    # Get prefix. If not on a server, no prefix is needed.
    #logging.message_log(message_in, message_in.guild.id)
    if message_in.guild:
        prefix = settings.prefix_get(message_in.guild.id)
        me = message_in.guild.me
    else:
        prefix = ""
        me = message_in.channel.me


    # Should we die? Check for exit command.
    if message_in.content == prefix + "exit" or message_in.content == "{} exit".format(me.mention):
        if settings.owners_check(message_in.author.id):
            sys.exit(0)

    # Check for cache contents command.
    if message_in.content.startswith(prefix + "cachecontents") or message_in.content.startswith("{} cachecontents".format(me.mention)):
        cacheCount = glob.glob("cache/{}_*".format(message_in.content.split(' ')[-1]))
        cacheString = '\n'.join(cacheCount)
        await message_in.channel.send(message_in.channel, "```{}```".format(cacheString))

    # Check each command loaded.
    for command in Bot.commands:
        # Do we have a command?
        if command_api.is_command(message_in, prefix, command):
            # Prevent message count increment.
            is_command = True

            # Send typing message.
            async with message_in.channel.typing():
                # Build message object.
                message_recv = message.Message
                message_recv.command = command.name
                if message_in.content.startswith("{} ".format(me.mention)):
                    message_recv.body = message_in.content.split("{} ".format(me.mention) + 
                                                                command.name, 1)[1]
                else:
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

    # Increment message counters if not command.
    if message_in.guild and not is_command:
        logging.message_log(message_in, message_in.guild.id)
        count = logging.message_count_get(message_in.guild.id)
        Bot.messagesSinceStart += 1
        count += 1

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
    bot.init()

    # Get our token to use.
    token = ""
    with open("token.txt") as m:
        token = m.read().strip()

    client.run(token)