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
from plugins import excuses

class TestExcuseSuite(unittest.TestCase):

    def testExcuseMsg(self):
        msg = message.message(body="")
        msg.command = "excuse"

        fullExcuseList = []

        for sorry in excuses.sorryList:
            for excuse in excuses.excuseList:
                fullExcuseList.append('*{} {}*'.format(sorryList[sorry], excuseList[excuse])
        
        result=excuses.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body in fullExcuseList, True)
