from api import command, message, plugin

def onInit(plugin_in):
    gitsrc_command = command.command(plugin, 'source', shortdesc='Get the git repo for the bot!')
    docs_command = command.command(plugin, 'docs', shortdesc='Get a link to the bot\'s documentation')
    tests_command = command.command(plugin, 'tests', shortdesc='Get a link to the bot\'s tests')
    return plugin.plugin(plugin, 'tinyurl', [gitsrc_command, docs_command, tests_command])

def onCommand(message_in):
    if message_in.command == 'source':
        return message.message(body="https://github.com/StarbotDiscord/Starbot")
    if message_in.command == 'docs':
        return message.message(body="http://starbot.readthedocs.io/en/latest/")
    if message_in.command == 'tests':
        return message.message(body="https://travis-ci.org/StarbotDiscord/Starbot")