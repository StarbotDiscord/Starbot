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