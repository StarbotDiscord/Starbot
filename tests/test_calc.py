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
from plugins import calc

class TestFunSuite(unittest.TestCase):

    def testCalcImport(self):
        result = calc.onInit(__import__('api.plugin'))
        self.assertEqual(type(result), plugin.plugin)



    def testCalcEmptyEqu(self):
        msg = message.message(body="")
        msg.command = "calc"
        result = calc.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testCalcInvalEqu(self):
        msg = message.message(body="banana")
        msg.command = "calc"
        result = calc.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testCalcValidEqu(self):
        msg = message.message(body="3+4")
        msg.command = "calc"
        result = calc.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "`3+4` = `7.0`")