import unittest

from api import command


class TestCommandSuite(unittest.TestCase):

    def testCommandBasicArgs(self):
        commandTest = command.command(unittest, 'testplugin')
        self.assertEqual(commandTest.name, 'testplugin')
        self.assertEqual(commandTest.plugin, unittest)
        self.assertEqual(commandTest.shortdesc, 'no description')
        self.assertEqual(commandTest.devcommand, False)

    def testCommandOverwrite(self):
        commandTest = command.command(unittest, 'testplugin')
        self.assertEqual(commandTest.name, 'testplugin')
        self.assertEqual(commandTest.plugin, unittest)
        self.assertEqual(commandTest.shortdesc, 'no description')
        self.assertEqual(commandTest.devcommand, False)

        commandTest = command.command(unittest, 'testplugin', shortdesc='python testing is fun!')
        self.assertEqual(commandTest.name, 'testplugin')
        self.assertEqual(commandTest.plugin, unittest)
        self.assertEqual(commandTest.shortdesc, 'python testing is fun!')
        self.assertEqual(commandTest.devcommand, False)

    def testCommandArgs(self):
        commandTest = command.command(unittest, 'testplugin', shortdesc='python testing is fun!', devcommand=True)
        self.assertEqual(commandTest.name, 'testplugin')
        self.assertEqual(commandTest.plugin, unittest)
        self.assertEqual(commandTest.shortdesc, 'python testing is fun!')
        self.assertEqual(commandTest.devcommand, True)

    def testCommandChangeArgs(self):
        commandTest = command.command(unittest, 'testplugin', shortdesc='python testing is fun!')
        self.assertEqual(commandTest.name, 'testplugin')
        self.assertEqual(commandTest.plugin, unittest)
        self.assertEqual(commandTest.shortdesc, 'python testing is fun!')
        self.assertEqual(commandTest.devcommand, False)

        commandTest.shortdesc = 'We\'ve changed the description!'
        self.assertEqual(commandTest.name, 'testplugin')
        self.assertEqual(commandTest.plugin, unittest)
        self.assertEqual(commandTest.shortdesc, 'We\'ve changed the description!')
        self.assertEqual(commandTest.devcommand, False)

if __name__ == '__main__':
    unittest.main()