Plugin.py Documentation
***********************

.. _api_bot:

Creating a plugin
=================

The bot class has a few variables in it you may find useful. See the code example below.
* `startTime` - the time the bot started up. (time.time())
* `plugins` - an array of plugins the bot has loaded. see :ref:`api_plugin`.
* `commands` - an array of commands the bot has loaded. see :ref:`api_command`.

.. code-block:: python
    :linenos:

    from api import bot

    bot.startTime #get the time the bot started up
    bot.plugins #get the array of plugins the bot has loaded
    bot.commands #get the array of commands the plugins have loaded