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
from plugins import search

class TestSearchSuite(unittest.TestCase):

    def testSearchEmptyMsg(self):
        msg = message.message(body="")
        msg.command = "google"
        result = yield from search.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, 'I need a topic to search for!')

    def testSearchGoogle(self):
        msg = message.message(body="hello world")
        msg.command = "google"
        result = yield from search.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        print(result)
        self.assertEqual(result.body, 'Google search: https://www.google.com/#q=hello%20world')
    
    def testSearchDuckDuckGo(self):
        msg = message.message(body="hello world")
        msg.command = "duckduckgo"
        result = yield from search.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "DuckDuckGo search: https://www.duckduckgo.com/?q=hello%20world")

    def testSearchBing(self):
        msg = message.message(body="hello world")
        msg.command = "bing"
        result = yield from search.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "Bing search: https://www.bing.com/?q=hello%20world")
