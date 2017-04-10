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
        result = tinyurl.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "http://tinyurl.com/cqvga")

    def testTinyurlInvalidURL(self):
        emptyList = []
        msg = message.message(body="test")
        msg.command = "tinyurl"
        result = tinyurl.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "Invalid URL")

    def testTinyurlEmptyURL(self):
        emptyList = []
        msg = message.message(body="")
        msg.command = "tinyurl"
        result = tinyurl.onCommand(msg)
        self.assertEqual(type(result), type(msg))