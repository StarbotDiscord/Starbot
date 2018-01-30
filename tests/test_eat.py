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
from api import message
from plugins import fun
from tests.fake_server import Server

class TestEatSuite(unittest.TestCase):

#    def test_testEatMsg(self):
#        server = fake_server
#        server.me = 'StarBot'
#        msg = message.Message(body="Food")
#        msg.command = "eat"
#        msg.server = server
#        result = eat.onCommand(msg)
#        itemList = ['*None*, you take a big chunk out of *Food*. *Delicious.*',
#                    '*None*, your teeth sink into *Food* - it tastes satisfying.',
#                    '*None*, you rip hungrily into *Food*, tearing it to bits!',
#                    '*None*, you just can\'t bring yourself to eat *Food* - so you just hold it for awhile...',
#                    '*None*, you attempt to bite into *Food*, but you\'re clumsier than you remember - and fail...']
#        self.assertEqual(type(result), type(msg))
#        self.assertEqual(result.body in nothingList, True)
        

    def test_eat_empty_msg(self):
        server = Server
        server.me = 'StarBot'
        msg = message.Message(body="")
        msg.command = "eat"
        msg.server = server
        result = yield from eat.onCommand(msg)
        nothing_list = ['*None*, you sit quietly and eat *nothing*...',
                        '*None*, you\'re *sure* there was something to eat, so you just chew on nothingness...',
                        '*None*, there comes a time when you need to realize that you\'re just chewing nothing\
                        for the sake of chewing.  That time is now.']
        print(result.body)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body in nothing_list, True)
