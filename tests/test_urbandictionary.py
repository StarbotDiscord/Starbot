import unittest
from api import message, plugin
from plugins import urbandictionary

class TestUrbanDictionarySuite(unittest.TestCase):

    def testUDImport(self):
        result = urbandictionary.onInit(__import__('api.plugin'))
        self.assertEqual(type(result), plugin.plugin)

    def testUDDefine(self):
        emptyList = []
        msg = message.message(body="test")
        msg.command = "define"
        result = urbandictionary.onCommand(msg)
        self.assertEqual(type(result), type(emptyList))

    def testUDDefineEmpty(self):
        emptyList = []
        msg = message.message(body="")
        msg.command = "define"
        result = urbandictionary.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testUDRandefine(self):
        emptyList = []
        msg = message.message(body="")
        msg.command = "randefine"
        result = urbandictionary.onCommand(msg)
        self.assertEqual(type(result), type(emptyList))