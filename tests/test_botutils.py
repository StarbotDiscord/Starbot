import unittest
from api import message, plugin, bot
from plugins import botutils

class TestBotutilsSuite(unittest.TestCase):

    def testSrcutilsImport(self):
        result = botutils.onInit(__import__('api.plugin'))
        self.assertEqual(type(result), plugin.plugin)


    def testBotutilsPlugins(self):
        result = botutils.onInit(__import__('api.plugin'))
        bot.bot.plugins.append(result)
        for command in result.commands:
            bot.bot.commands.append(command)

        msg = message.message(body="")
        msg.command = "plugins"
        result = botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))


    def testBotutilsCommands(self):
        result = botutils.onInit(__import__('api.plugin'))
        bot.bot.plugins.append(result)
        for command in result.commands:
            bot.bot.commands.append(command)

        msg = message.message(body="")
        msg.command = "commands"
        result = botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testBotutilsHelp(self):
        result = botutils.onInit(__import__('api.plugin'))
        bot.bot.plugins.append(result)
        for command in result.commands:
            bot.bot.commands.append(command)

        msg = message.message(body="")
        msg.command = "help"
        result = botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testBotutilsInfo(self):
        msg = message.message(body="")
        msg.command = "info"
        result = botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testBotutilsPlugintree(self):
        msg = message.message(body="")
        msg.command = "plugintree"
        result = botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testBotutilsUptime(self):
        msg = message.message(body="")
        msg.command = "uptime"
        result = botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testBotutilsHostinfo(self):
        msg = message.message(body="")
        msg.command = "hostinfo"
        result = botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testBotutilsCpuinfo(self):
        msg = message.message(body="")
        msg.command = "cpuinfo"
        result = botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))
