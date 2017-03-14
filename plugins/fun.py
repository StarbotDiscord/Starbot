import plugin
import command
import message
import random

# Fun plugin
def onInit(plugin):
    lenny_command = command.command(plugin, 'lenny', shortdesc='Give some Lenny')
    shrug_command = command.command(plugin, 'shrug', shortdesc='Shrug it off')
    tableflip_command = command.command(plugin, 'tableflip', shortdesc='Flip a table')
    fart_command = command.command(plugin, 'fart', shortdesc='PrincessZoey :P')
    return plugin.plugin.plugin(plugin, 'fun', [say_command, lenny_command, shrug_command, tableflip_command, fart_command])

def onCommand(message_in):
    # Lenny.
    if message_in.command == 'lenny':
        # Create message.
        msg = "( ͡° ͜ʖ ͡°)"

        # Append extra on if needed.
        if message_in.body.strip():
            msg += "\n" + message_in.body.strip()

        # Return message.
        return message.message(msg, delete=True)

    # Shrug.
    if message_in.command == 'shrug':
        # Create message.
        msg = "¯\_(ツ)_/¯"

        # Append extra on if needed.
        if message_in.body.strip():
            msg += "\n" + message_in.body.strip()

        # Return message.
        return message.message(msg, delete=True)

    # Tableflip.
    if message_in.command == 'tableflip':
        # Create message.
        msg = "(╯°□°）╯︵ ┻━┻"

        # Append extra on if needed.
        if message_in.body.strip():
            msg += "\n" + message_in.body.strip()

        # Return message.
        return message.message(msg, delete=True)

    # Fart.
    if message_in.command == 'fart':
        # Make farts.
        fartList = ["Poot", "Prrrrt", "Thhbbthbbbthhh", "Plllleerrrrffff", "Toot", "Blaaaaahnk", "Squerk"]
        randnum = random.randint(0, len(fartList)-1)
        msg = '{}'.format(fartList[randnum])

        # Append extra on if needed.
        if message_in.body.strip():
            msg += "\n" + message_in.body.strip()

        # Return fart message.
        return message.message(msg, delete=True)
