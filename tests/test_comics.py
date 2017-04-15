import unittest
from api import message, plugin
from plugins import comics

class TestFunSuite(unittest.TestCase):

    def testComicsImport(self):
        result = comics.onInit(__import__('api.plugin'))
        self.assertEqual(type(result), plugin.plugin)



    def testComicsXKCDEmptyID(self):
        msg = message.message(body="")
        msg.command = "xkcd"
        result = comics.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testComicsXKCDWithID(self):
        msg = message.message(body="303")
        msg.command = "xkcd"
        result = comics.onCommand(msg)
        self.assertEqual(type(result), type(msg))