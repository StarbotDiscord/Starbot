import unittest
import command
import plugin

class TestCommandSuite(unittest.TestCase):

    def testPluginBasicArgs(self):
        commandTest = command.command(unittest, 'TestCommand')
        pluginTest = plugin.plugin(unittest, 'TestPlugin', [commandTest])
        self.assertEqual(pluginTest.plugin, unittest)
        self.assertEqual(pluginTest.name, 'TestPlugin')
        self.assertEqual(pluginTest.commands, [commandTest])

    def testPluginOverwrite(self):
        commandTest = command.command(unittest, 'TestCommand')
        pluginTest = plugin.plugin(unittest, 'TestPlugin', [commandTest])
        self.assertEqual(pluginTest.plugin, unittest)
        self.assertEqual(pluginTest.name, 'TestPlugin')
        self.assertEqual(pluginTest.commands, [commandTest])

        commandTest2 = command.command(unittest, 'TestCommand', shortdesc='Description!')
        pluginTest = plugin.plugin(unittest, 'TestPlugin', [commandTest2])
        self.assertEqual(pluginTest.plugin, unittest)
        self.assertEqual(pluginTest.name, 'TestPlugin')
        self.assertEqual(pluginTest.commands, [commandTest2])
        self.assertEqual(pluginTest.commands[0].shortdesc, 'Description!')