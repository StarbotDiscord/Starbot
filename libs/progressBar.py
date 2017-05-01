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

def makeBar(progress):
    # Get the progress in half for a shorter progress bar
    shortProgress = progress/2
    # Convert progress to a string while we are at it
    progressString = str(progress)

    # Get the amount of "done" progress, or the % of 100%
    doneProgress = int(shortProgress)
    # Get the reverse of above, for the % of 100% not done
    undoneProgress = 50-int(shortProgress)

    # We fill the percentage done with # characters
    doneString = '#'*doneProgress
    # The rest with whitespaces
    undoneString = ' '*undoneProgress

    # Build our progress bar and return it
    return '[{}{}] {}%'.format(doneString, undoneString, progressString.rjust(5))