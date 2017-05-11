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
from plugins import cacheutils

class TestCacheSuite(unittest.TestCase):

    def testSrcutilsImport(self):
        result = cacheutils.onInit(__import__('api.plugin'))
        self.assertEqual(type(result), plugin.plugin)



    def testCacheutilsCachecount(self):
        msg = message.message(body="")
        msg.command = "cachecount"
        result = yield from cacheutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testCacheutilsCaches(self):
        msg = message.message(body="")
        msg.command = "caches"
        result = yield from cacheutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testCachecountTotalcache(self):
        msg = message.message(body="")
        msg.command = "totalcache"
        result = yield from cacheutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))