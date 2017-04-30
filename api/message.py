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

class message:
    def __init__(self, body='', file='', embed=None, author=None, server=None, delete=False, mentions=None):
        self.command = None
        self.author = None
        self.server = None
        self.body = body
        self.file = file
        self.embed = embed
        self.delete = delete
        self.mentions = mentions