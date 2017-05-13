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

from api import command

class TestCommandSuite(unittest.TestCase):

    def test_command_basic_args(self):
        cmd_test = command.Command(unittest, 'testplugin')
        self.assertEqual(cmd_test.name, 'testplugin')
        self.assertEqual(cmd_test.plugin, unittest)
        self.assertEqual(cmd_test.shortdesc, 'no description')
        self.assertEqual(cmd_test.devcommand, False)

    def test_command_overwrite(self):
        cmd_test = command.Command(unittest, 'testplugin')
        self.assertEqual(cmd_test.name, 'testplugin')
        self.assertEqual(cmd_test.plugin, unittest)
        self.assertEqual(cmd_test.shortdesc, 'no description')
        self.assertEqual(cmd_test.devcommand, False)

        cmd_test = command.Command(unittest, 'testplugin', shortdesc='python testing is fun!')
        self.assertEqual(cmd_test.name, 'testplugin')
        self.assertEqual(cmd_test.plugin, unittest)
        self.assertEqual(cmd_test.shortdesc, 'python testing is fun!')
        self.assertEqual(cmd_test.devcommand, False)

    def test_command_args(self):
        cmd_test = command.Command(unittest, 'testplugin', shortdesc='python testing is fun!', devcommand=True)
        self.assertEqual(cmd_test.name, 'testplugin')
        self.assertEqual(cmd_test.plugin, unittest)
        self.assertEqual(cmd_test.shortdesc, 'python testing is fun!')
        self.assertEqual(cmd_test.devcommand, True)

    def test_command_change_args(self):
        cmd_test = command.Command(unittest, 'testplugin', shortdesc='python testing is fun!')
        self.assertEqual(cmd_test.name, 'testplugin')
        self.assertEqual(cmd_test.plugin, unittest)
        self.assertEqual(cmd_test.shortdesc, 'python testing is fun!')
        self.assertEqual(cmd_test.devcommand, False)

        cmd_test.shortdesc = 'We\'ve changed the description!'
        self.assertEqual(cmd_test.name, 'testplugin')
        self.assertEqual(cmd_test.plugin, unittest)
        self.assertEqual(cmd_test.shortdesc, 'We\'ve changed the description!')
        self.assertEqual(cmd_test.devcommand, False)

if __name__ == '__main__':
    unittest.main()