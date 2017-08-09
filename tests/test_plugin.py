#    Copyright 2017 Starbot Discord Project
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import unittest

from api import command, plugin


class TestCommandSuite(unittest.TestCase):

    def test_plugin_basic_args(self):
        cmd_test = command.Command(unittest, 'TestCommand')
        plugin_test = plugin.Plugin(unittest, 'TestPlugin', [cmd_test])
        self.assertEqual(plugin_test.plugin, unittest)
        self.assertEqual(plugin_test.name, 'TestPlugin')
        self.assertEqual(plugin_test.commands, [cmd_test])

    def test_plugin_overwrite(self):
        cmd_test = command.Command(unittest, 'TestCommand')
        plugin_test = plugin.Plugin(unittest, 'TestPlugin', [cmd_test])
        self.assertEqual(plugin_test.plugin, unittest)
        self.assertEqual(plugin_test.name, 'TestPlugin')
        self.assertEqual(plugin_test.commands, [cmd_test])

        cmd_test2 = command.Command(unittest, 'TestCommand', shortdesc='Description!')
        plugin_test = plugin.Plugin(unittest, 'TestPlugin', [cmd_test2])
        self.assertEqual(plugin_test.plugin, unittest)
        self.assertEqual(plugin_test.name, 'TestPlugin')
        self.assertEqual(plugin_test.commands, [cmd_test2])
        self.assertEqual(plugin_test.commands[0].shortdesc, 'Description!')
