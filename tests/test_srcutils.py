import unittest
from api import message, plugin
from plugins import srcutils

class TestFunSuite(unittest.TestCase):

    def testSrcutilsImport(self):
        result = srcutils.onInit(__import__('api.plugin'))
        self.assertEqual(type(result), plugin.plugin)



    def testSrcutilsSource(self):
        msg = message.message(body="")
        msg.command = "source"
        result = srcutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testSrcutilsDocs(self):
        msg = message.message(body="")
        msg.command = "docs"
        result = srcutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testSrcutilsTests(self):
        msg = message.message(body="")
        msg.command = "tests"
        result = srcutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "`3+4` = `7.0`")