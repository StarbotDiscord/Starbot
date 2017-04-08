Message.py Documentation
************************

Creating a message
==================

You can create a message that contains:

* A body of text
* A file
* A body of text and a file
* An embed (one of dem darned fancy thingy-majiggies like in the !info command)

Creating a text based message
+++++++++++++++++++++++++++++

Let's create a message with some funny text to send to our friends in the server!

.. code-block:: python
    :linenos:

    from api import message

    new_message = message.message(body="Code runs faster when Chuck Norris watches it.")

Creating a file based message
+++++++++++++++++++++++++++++

How about if we want to send a photo of our cat doing a funny pose?

.. code-block:: python
    :linenos:

    from api import message

    new_message = message.message(file="imgs/funny_cat_photo.png")

Creating a text and file based message
++++++++++++++++++++++++++++++++++++++

Let's try sending our cat photo and our funny joke!

.. code-block:: python
    :linenos:

    from api import message

    new_message = message.message(body="Code runs faster when Chuck Norris watches it.",
        file="imgs/funny_cat_photo.png")

Sending a message
=================

It's great and all that we can make messages, but they aren't showing up! How do I make my messages show up in Discord?

Your message should be returned when your plugin's function is called. Try this out!

.. code-block:: python
    :linenos:

    from api import command, message, plugin

    def onInit(plugin):
        chuckjoke_command = command.command(plugin, 'chuckjoke', shortdesc='Print our funny chuck norris joke!')
        return plugin.plugin.plugin(plugin, 'chuck_norris', [chuckjoke_command])

    def onCommand(message_in):
        new_message = message.message(body="Code runs faster when Chuck Norris watches it.")
        return new_message