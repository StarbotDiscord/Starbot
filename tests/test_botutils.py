import unittest
from api import message, plugin
from plugins import botutils

class TestFunSuite(unittest.TestCase):

    def testSrcutilsImport(self):
        result = botutils.onInit(__import__('api.plugin'))
        self.assertEqual(type(result), plugin.plugin)


    def testBotutilsPlugins(self):
        msg = message.message(body="")
        msg.command = "plugins"
        result = botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))


    def testBotutilsCommands(self):
        msg = message.message(body="")
        msg.command = "commands"
        result = botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testBotutilsHelp(self):
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
