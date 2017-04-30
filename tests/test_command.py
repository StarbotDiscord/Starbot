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