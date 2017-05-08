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

import random
from api import command, message, plugin

def onInit(plugin_in):
    excuse_command = command.command(plugin_in, 'excuse', shortdesc='Dish out excuses ;)')
    return plugin.plugin(plugin_in, 'excuses', [excuse_command])

async def onCommand(message_in):
    if message_in.command == 'excuse':
        # Give excuses
        excuseList = ["I have an appointment with a robot.", 
        "I was abducted by robots.", 
        "I didn’t know what day it was because I was looking at the Robotic Calendar.",
        "My robot threw up on my source code.", 
        "I need to take my robot for a walk.",
        "I had to get a cybernetic head and couldn't get anything done.",
        "My Robot Assistant blue-screened.",
        "A kernel panic erased my work.",
        "Somebody used up the data limit watching YouTube."]
        randexcuse = random.randint(0, len(excuseList)-1)
        
        # Say sorry
        sorryList = ["Please excuse me,", "I'm sorry, but", "I hope you forgive me, because"]
        randsorry = random.randint(0, len(sorryList)-1)

        msg = '*{} {}*'.format(sorryList[randsorry], excuseList[randexcuse])

        # Return newly constructed message
        return message.message(msg)