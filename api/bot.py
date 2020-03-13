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

from typing import List
from api.command import Command
from api.plugin import Plugin
import discord

class Bot:
    startTime:          float = 0.0
    plugins:            List[Plugin] = []
    commands:           List[Command] = []
    messagesSinceStart: int = 0
    client:             discord.Client = None

    version_major:      int = 0
    version_minor:      int = 3
    version_revision:   int = 0
    version:            str = str(version_major) + "." + str(version_minor) + "." + str(version_revision)