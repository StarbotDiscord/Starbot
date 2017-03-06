import plugin
import command
import message
from urllib.request import urlopen

def onInit(plugin):
    tinyurl_command = command.command(plugin, 'tinyurl')
    return plugin.plugin.plugin(plugin, 'tinyurl', [tinyurl_command])

def onCommand(message_in):
    return message.create(body=urlopen("http://tinyurl.com/api-create.php?url=" + message_in.body.strip()).read().decode("utf-8"))