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
from api import message, plugin
from plugins import fun

class TestFunSuite(unittest.TestCase):

    def testFunImport(self):
        result = fun.onInit(__import__('api.plugin'))
        self.assertEqual(type(result), plugin.plugin)



    def testFunLennyEmptyMsg(self):
        msg = message.Message(body="")
        msg.command = "lenny"
        result = yield from fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "( ͡° ͜ʖ ͡°)")

    def testFunLennyMsg(self):
        msg = message.Message(body="hi")
        msg.command = "lenny"
        result = yield from fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "( ͡° ͜ʖ ͡°)\nhi")



    def testFunShrugEmptyMsg(self):
        msg = message.Message(body="")
        msg.command = "shrug"
        result = yield from fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "¯\_(ツ)_/¯")

    def testFunShrugMsg(self):
        msg = message.Message(body="hi")
        msg.command = "shrug"
        result = yield from fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "¯\_(ツ)_/¯\nhi")



    def testFunFartMsg(self):
        msg = message.Message(body="")
        msg.command = "fart"
        result = yield from fun.onCommand(msg)
        fartList = ["Poot", "Prrrrt", "Thhbbthbbbthhh", "Plllleerrrrffff", "Toot", "Blaaaaahnk", "Squerk"]
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body in fartList, True)



    def testFunBetaMsg(self):
        msg = message.Message(body="")
        msg.command = "beta"
        result = yield from fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, 'It looks like something went wrong')
        self.assertEqual(result.file, 'beta.jpg')