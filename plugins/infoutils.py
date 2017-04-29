import discord

from api import command, message, plugin
from libs import displayname

# Command names.
SERVERINFO = "serverinfo"
EMOTEINFO = "emoteinfo"

def SortEmote(e):
    return e.name

def onInit(plugin_in):
    serverinfo_command = command.command(plugin_in, SERVERINFO, shortdesc="Show info about this server")
    emoteinfo_command = command.command(plugin_in, EMOTEINFO, shortdesc="Show the emotes on this server")
    return plugin.plugin(plugin_in, "infoutils", [serverinfo_command, emoteinfo_command])

def onCommand(message_in):
    if message_in.command == SERVERINFO:
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
        voice_channels = [c.name for c in server.channels if str(c.type) == "voice"]
        text_channels = [c.name for c in server.channels if str(c.type) == "text"]
        server_embed.add_field(name="Channels", value="{} text, {} voice".format(len(text_channels), len(voice_channels)))
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
        return message.message("**Server Info:**", embed=server_embed)

    if message_in.command == EMOTEINFO:       
        # Get emotes.
        emotelist = ""
        for emote in sorted(message_in.server.emojis, key=SortEmote):
            emotelist += str(emote) + " "

        # Return message.
        return message.message("**{}** emotes:\n{}".format(message_in.server.name, emotelist))
        