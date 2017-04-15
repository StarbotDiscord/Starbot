import unittest
from api import message, plugin
from plugins import fun

class TestFunSuite(unittest.TestCase):

    def testFunImport(self):
        result = fun.onInit(__import__('api.plugin'))
        self.assertEqual(type(result), plugin.plugin)



    def testFunLennyEmptyMsg(self):
        msg = message.message(body="")
        msg.command = "lenny"
        result = fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "( ͡° ͜ʖ ͡°)")

    def testFunLennyMsg(self):
        msg = message.message(body="hi")
        msg.command = "lenny"
        result = fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "( ͡° ͜ʖ ͡°)\nhi")



    def testFunShrugEmptyMsg(self):
        msg = message.message(body="")
        msg.command = "shrug"
        result = fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "¯\_(ツ)_/¯")

    def testFunShrugMsg(self):
        msg = message.message(body="hi")
        msg.command = "shrug"
        result = fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "¯\_(ツ)_/¯\nhi")



    def testFunFartMsg(self):
        msg = message.message(body="")
        msg.command = "fart"
        result = fun.onCommand(msg)
        fartList = ["Poot", "Prrrrt", "Thhbbthbbbthhh", "Plllleerrrrffff", "Toot", "Blaaaaahnk", "Squerk"]
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body in fartList, True)



    def testFunBetaMsg(self):
        msg = message.message(body="")
        msg.command = "beta"
        result = fun.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, 'It looks like something went wrong')
        self.assertEqual(result.file, 'beta.jpg')