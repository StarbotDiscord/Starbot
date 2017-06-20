Plugin.py Documentation
***********************

.. _api_plugin:

Creating a plugin
=================

A plugin can take the following arguments, of which *all* are mandatory:

* `plugin` - this is the plugin's module. onInit will take this as an argument, so just pass it back.
* `name` - a string containing the name of your plugin, which should be the filename
* `commands` - an array of commands in your plugin. see :ref:`api_command`.

.. code-block:: python
    :linenos:

    from api import plugin

    new_plugin = plugin.Plugin(plugin=plugin_in,
        name="testplugin"
        commands=[my_command, my_other_command])