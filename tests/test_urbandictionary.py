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
from plugins import urbandictionary

class TestUrbanDictionarySuite(unittest.TestCase):

    def test_ud_import(self):
        result = urbandictionary.onInit(__import__('api.plugin'))
        self.assertEqual(type(result), plugin.Plugin)

    def test_ud_define(self):
        empty_list = []
        msg = message.Message(body="test")
        msg.command = "define"
        result = yield from urbandictionary.onCommand(msg)
        self.assertEqual(type(result), type(empty_list))

    def test_ud_define_empty(self):
        msg = message.Message(body="")
        msg.command = "define"
        result = yield from urbandictionary.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def test_ud_randefine(self):
        emptyList = []
        msg = message.Message(body="")
        msg.command = "randefine"
        result = yield from urbandictionary.onCommand(msg)
        self.assertEqual(type(result), type(emptyList))
