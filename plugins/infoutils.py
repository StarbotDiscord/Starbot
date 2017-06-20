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

import discord

from api import command, message, plugin
from api.bot import Bot
from libs import displayname

# Command names.
SERVERINFOCMD = "serverinfo"
EMOTEINFOCMD = "emoteinfo"
SERVERINVITECMD = "serverinvite"

def SortEmote(e):
    return e.name

def onInit(plugin_in):
    serverinfo_command = command.Command(plugin_in, SERVERINFOCMD, shortdesc="Show info about this server")
    emoteinfo_command = command.Command(plugin_in, EMOTEINFOCMD, shortdesc="Show the emotes on this server")
    serverinvite_command = command.Command(plugin_in, SERVERINVITECMD, shortdesc="Get an invite link to this server")
    return plugin.Plugin(plugin_in, "infoutils", [serverinfo_command, emoteinfo_command, serverinvite_command])

async def onCommand(message_in):
    if message_in.command == SERVERINFOCMD:
        # Get server.
        server = message_in.server

        # Create blank embed.
        server_embed = discord.Embed(color=server.me.color)

        # Add title of server and icon.
        server_embed.title = server.name
        server_embed.description = "Created at {} UTC".format(server.created_at.strftime("%Y-%m-%d %I:%M %p"))
        server_embed.set_thumbnail(url=server.icon_url)

        # Add members and role count.
        server_embed.add_field(name="Members", value=str(server.member_count))
        server_embed.add_field(name="Roles", value=str(len(server.roles)), inline=True)

        # Add channel count and default channel.
        channels_voice = [c.name for c in server.channels if str(c.type) == "voice"]
        channels_text = [c.name for c in server.channels if str(c.type) == "text"]
        server_embed.add_field(name="Channels", value="{} text, {} voice".format(len(channels_text), len(channels_voice)))
        server_embed.add_field(name="Default Channel", value=server.default_channel.mention, inline=True)

        # Add region and AFK.
        server_embed.add_field(name="Voice Region", value=server.region)
        if server.afk_channel != None:
            server_embed.add_field(name="AFK Channel", value="{} after {} minutes".format(server.afk_channel.name, int(server.afk_timeout / 60)))
        else:
            server_embed.add_field(name="AFK Channel", value="None")

        # Add verification and owner.
        server_embed.add_field(name="Verification", value=str(server.verification_level))
        server_embed.add_field(name="Owner", value=server.owner.mention, inline=True)

        # Add server ID to footer.
        server_embed.set_footer(text="Server ID: {}".format(server.id))
        return message.Message("**Server Info:**", embed=server_embed)

    if message_in.command == EMOTEINFOCMD:
        # Get emotes.
        emotelist = ""
        for emote in sorted(message_in.server.emojis, key=SortEmote):
            emotelist += str(emote) + " "

        # Return message.
        return message.Message("**{}** emotes:\n{}".format(message_in.server.name, emotelist))

    if message_in.command == SERVERINVITECMD:
        # Check that we have perms to create an invite. If not, return error.
        if not message_in.server.default_channel.permissions_for(message_in.server.me).create_instant_invite:
            return message.Message("Whoops I don't have permission to create instant invites for this server.")

        # Create invite and return message.
        invite = await Bot.client.create_invite(message_in.server.default_channel, unique=False)
        return message.Message("Use this link to invite people to this server: {}".format(invite.url))
        