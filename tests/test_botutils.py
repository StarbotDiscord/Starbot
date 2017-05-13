#    Copyright 2017 Starbot Discord Project
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import unittest
from api import message, plugin, bot
from plugins import botutils
from tests import fake_server

class TestBotutilsSuite(unittest.TestCase):

    def testSrcutilsImport(self):
        result = botutils.onInit(__import__('api.plugin'))
        self.assertEqual(type(result), plugin.Plugin)


    def testBotutilsPlugins(self):
        result = botutils.onInit(__import__('api.plugin'))
        bot.Bot.plugins.append(result)
        for command in result.commands:
            bot.Bot.commands.append(command)

        msg = message.Message(body="")
        msg.command = "plugins"
        result = yield from botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))


    def testBotutilsCommands(self):
        result = botutils.onInit(__import__('api.plugin'))
        bot.Bot.plugins.append(result)
        for command in result.commands:
            bot.Bot.commands.append(command)

        msg = message.Message(body="")
        msg.command = "commands"
        result = yield from botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testBotutilsHelp(self):
        result = botutils.onInit(__import__('api.plugin'))
        bot.Bot.plugins.append(result)
        for command in result.commands:
            bot.Bot.commands.append(command)

        msg = message.Message(body="")
        msg.command = "help"
        result = yield from botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testBotutilsInfo(self):
        msg = message.Message(body="")
        msg.command = "info"
        result = yield from botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testBotutilsPlugintree(self):
        msg = message.Message(body="")
        msg.command = "plugintree"
        result = yield from botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testBotutilsUptime(self):
        msg = message.Message(body="")
        msg.command = "uptime"
        result = yield from botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testBotutilsHostinfo(self):
        server = fake_server
        server.me = 'StarBot'

        msg = message.Message(body="")
        msg.command = "hostinfo"
        msg.server = server

        result = yield from botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testBotutilsCpuinfo(self):
        msg = message.Message(body="")
        msg.command = "cpuinfo"
        result = yield from botutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))
