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
from plugins import tinyurl

class TestTinyurlSuite(unittest.TestCase):

    def testTinyurlImport(self):
        result = tinyurl.onInit(__import__('api.plugin'))
        self.assertEqual(type(result), plugin.plugin)

    def testTinyurlValidURL(self):
        emptyList = []
        msg = message.message(body="https://www.google.com/")
        msg.command = "tinyurl"
        result = yield from tinyurl.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "http://tinyurl.com/cqvga")

    def testTinyurlInvalidURL(self):
        emptyList = []
        msg = message.message(body="test")
        msg.command = "tinyurl"
        result = yield from tinyurl.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "That website doesn't seem to exist")

    def testTinyurlEmptyURL(self):
        emptyList = []
        msg = message.message(body="")
        msg.command = "tinyurl"
        result = yield from tinyurl.onCommand(msg)
        self.assertEqual(type(result), type(msg))