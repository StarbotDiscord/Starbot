Command.py Documentation
************************

.. _api_command:

Creating a command
==================

A command can take the following arguments, of which *the first two* are mandatory:

* `plugin` - this is the plugin's module. onInit will take this as an argument, so just pass it back. see :ref:`api_plugin`.
* `name` - a string containing the name of your command, which will be what the bot uses to determine if your command is run.
* `shortdesc` - a string to describe your command, which will show in !help and !commands
* `devcommand` - whether or not the command should be hidden from !help and !commands. By default this is false.

.. code-block:: python
    :linenos:

    from api import plugin

    new_command = plugin.Plugin(plugin=plugin_in,
        name="my_command"
        shortdesc="look mom, i made a command!",
        devcommand=False)