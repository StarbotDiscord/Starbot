Getting Started with Plugin Writing
***********************************

.. _getstarted_pluginwriting:

Some useful links
=================

* :ref:`api_plugin`
* :ref:`api_command`
* :ref:`api_message`

A basic plugin - text manipulation
==================================

.. code-block:: python
    :linenos:

    from api import command, message, plugin

    def onInit(plugin_in):
        tolower_command = command.command(plugin_in,
            'tolower',
            shortdesc='Convert text to lower case')

        toupper_command = command.command(plugin_in,
            'toupper',
            shortdesc='Convert text to upper case')

        return plugin.plugin(plugin_in, 'texttools', [tolower_command])

    def onCommand(message_in):
        if message_in.command == 'tolower':
            msg = message_in.body.lower()
            return message.message(body=msg)

        elif message_in.command == 'toupper':
            msg = message_in.body.upper()
            return message.message(body=msg)