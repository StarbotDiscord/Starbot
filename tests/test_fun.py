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

    def test_fun_import(self):
        result = fun.onInit(__import__('api.plugin'))
        self.assertEqual(type(result), plugin.Plugin)

    def test_fun_lenny_empty_msg(self):
        msg = message.Message(body="")
        msg.command = "lenny"
        result = yield from fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "( ͡° ͜ʖ ͡°)")

    def test_fun_lenny_msg(self):
        msg = message.Message(body="hi")
        msg.command = "lenny"
        result = yield from fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "( ͡° ͜ʖ ͡°)\nhi")

    def test_fun_shrug_empty_msg(self):
        msg = message.Message(body="")
        msg.command = "shrug"
        result = yield from fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, r"¯\_(ツ)_/¯")

    def test_fun_shrug_msg(self):
        msg = message.Message(body="hi")
        msg.command = "shrug"
        result = yield from fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, r"¯\_(ツ)_/¯\nhi")

    def test_fun_fart_msg(self):
        msg = message.Message(body="")
        msg.command = "fart"
        result = yield from fun.onCommand(msg)
        msg_list = ["Poot", "Prrrrt", "Thhbbthbbbthhh", "Plllleerrrrffff", "Toot", "Blaaaaahnk", "Squerk"]
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body in msg_list, True)

    def test_fun_beta_msg(self):
        msg = message.Message(body="")
        msg.command = "beta"
        result = yield from fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, 'It looks like something went wrong')
        self.assertEqual(result.file, 'beta.jpg')
