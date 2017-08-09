Message.py Documentation
************************

.. _api_message:

Creating a message
==================

A message can take the following arguments:

* `body` - a string to send
* `file` - a path to a file to upload, relative to the root folder of the bot
* `embed` - an embed for Discord

.. code-block:: python
    :linenos:

    from api import message

    new_message = message.Message(body="Code runs faster when Chuck Norris watches it.",
        file="imgs/funny_cat_photo.png",
        embed=embed)

Sending a message
=================

The bot expects you to return a message when your onCommand function is called. If you do not, the command's execution
will be considered unsuccessful and an error message will be sent to the channel.