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

def getCommit():
    if getBranch() == "UNKNOWN":
        return "UNKNOWN"
    else:
        with open(".git/refs/heads/{}".format(getBranch())) as e:
            commit = e.read()
            return commit.strip()

def getBranch():
    with open(".git/HEAD") as f:
        HEADFileS = f.read()
        HFileA = HEADFileS.split(": ")
        if len(HFileA) == 2:
            branch = HFileA[1].split("/", 2)[-1]
            return branch.strip()
        else:
            return "UNKNOWN"
