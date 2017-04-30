import unittest
from api import message, plugin
from plugins import eat
from tests import fake_server

class TestEatSuite(unittest.TestCase):

#    def testEatMsg(self):
#        server = fake_server
#        server.me = 'StarBot'
#        msg = message.message(body="Food")
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
        

    def testEatEmptyMsg(self):
        server = fake_server
        server.me = 'StarBot'
        msg = message.message(body="")
        msg.command = "eat"
        msg.server = server
        result = eat.onCommand(msg)
        nothingList = [ '*None*, you sit quietly and eat *nothing*...',
                        '*None*, you\'re *sure* there was something to eat, so you just chew on nothingness...',
                        '*None*, there comes a time when you need to realize that you\'re just chewing nothing for the sake of chewing.  That time is now.']
        print(result.body)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body in nothingList, True)
