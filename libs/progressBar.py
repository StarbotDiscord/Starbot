# Copyright (c) 2017 CorpNewt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

def makeBar(progress):
    return '[{0}{1}] {2}%'.format('#'*(int(round(progress/2))), ' '*(50-(int(round(progress/2)))), str(progress).rjust(5))