from api.bot import Bot

from glob import glob
import importlib

def init():
    for name in glob("plugins/*.py"):
        p = importlib.import_module("plugins." + name[8:-3])
        initPlugin(p)

def initPlugin(plugin):
    # Init plugin.
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