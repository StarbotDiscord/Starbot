import time

from pluginbase import PluginBase

from api import database
from api.bot import Bot

def init():
    database.init()

    # Log the time we started.
    Bot.startTime = time.time()

    # Get the source of plugins.
    plugin_base = PluginBase(package="plugins")
    plugin_source = plugin_base.make_plugin_source(searchpath=["./plugins"])

    # Load each plugin.
    for plugin in plugin_source.list_plugins():
        initPlugin(plugin_source, plugin)

def initPlugin(plugin_source, plugin, autoImport=True):
    # Init plugin.
    if autoImport == True:
        plugin_temp = plugin_source.load_plugin(plugin)
        plugin_info = plugin_temp.onInit(plugin_temp)
    else:
        plugin_info = plugin.onInit(plugin)

    # Verify the plugin is defined, it has a name, and it has commands.
    if plugin_info.plugin == None:
        print("[ERR ] Plugin not defined!")
        pass
    if plugin_info.name == None:
        print("[ERR ] Plugin name not defined")
        pass
    if plugin_info.commands == []:
        print("[WARN] Plugin did not define any commands.")

    # Add plugin to list.
    Bot.plugins.append(plugin_info)

    # Load each command in plugin.
    for command in plugin_info.commands:
        # Verify command has a parent plugin and a name.
        if command.plugin == None:
            print("[ERR ] Plugin command does not define parent plugin")
            pass
        if command.name == None:
            print("[ERR ] Plugin command does not define name")
            pass
        if command.func == None:
            print("[ERR ] Plugin command does not define function to call")
            pass

        # Add command to list of commands and print a success message.
        Bot.commands.append(command)
        print("Command `{}` registered successfully.".format(command.name))

    # Print success message.
    print("Plugin '{}' registered successfully.".format(plugin_info.name))