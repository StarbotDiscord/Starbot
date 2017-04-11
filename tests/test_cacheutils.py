import unittest
from api import message, plugin
from plugins import cacheutils

class TestFunSuite(unittest.TestCase):

    def testSrcutilsImport(self):
        result = cacheutils.onInit(__import__('api.plugin'))
        self.assertEqual(type(result), plugin.plugin)



    def testCacheutilsCachecount(self):
        msg = message.message(body="")
        msg.command = "cachecount"
        result = cacheutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testCacheutilsCaches(self):
        msg = message.message(body="")
        msg.command = "caches"
        result = cacheutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))

    def testCachecountTotalcache(self):
        msg = message.message(body="")
        msg.command = "totalcache"
        result = cacheutils.onCommand(msg)
        self.assertEqual(type(result), type(msg))
        self.assertEqual(result.body, "`3+4` = `7.0`")