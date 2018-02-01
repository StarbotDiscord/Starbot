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
'''Get current git branch and commit'''

def git_commit():
    '''Get the current git commit.'''
    if git_branch() == "UNKNOWN":
        return "UNKNOWN"
    else:
        with open(".git/refs/heads/{}".format(git_branch())) as file:
            commit = file.read()
            return commit.strip()

def git_branch():
    '''Get the current git branch.'''
    with open(".git/HEAD") as file:
        head_string = file.read()
        head_split = head_string.split(": ")
        if len(head_split) == 2:
            branch = head_split[1].split("/", 2)[-1]
            msg = branch.strip()
        else:
            msg = "UNKNOWN"
    return msg

def get_remote():
    with open(".git/config") as f:
        content = f.readlines()
        for line in content:
            if line.startswith('\turl'):
                return line.split("url = ")[1].strip()

def get_url():
    with open(".git/config") as f:
        content = f.readlines()
        for line in content:
            if line.startswith('\turl'):
                url = line.split("url = ")[1].strip()[:-4]
                slash = "/"
                return url + slash

            
            
            
