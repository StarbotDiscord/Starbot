import plugin
import command
import message

import glob
import os.path

def onInit(plugin_in):
    build_command   = command.command(plugin_in, 'build',    shortdesc='Print a list of a user\'s builds', devcommand=True)
    addbuild_command = command.command(plugin_in, 'addbuild', shortdesc='Add a build to your list',        devcommand=True)
    return plugin.plugin(plugin_in, 'parts', [build_command, addbuild_command])

def onCommand(message_in):
    if message_in.command == 'build':
        argsList = message_in.body[1:].split(' ', 1)
        if argsList[0] == '':
            userBuilds = glob.glob('cache/build_{}_*.txt'.format(message_in.author))
            print(userBuilds)
            if len(userBuilds) != 0:
                buildsList = []
                for build in userBuilds:
                    buildsList.append(build.replace('\\', '/').split("cache/build_{}_".format(message_in.author))[1][:4])
                print(buildsList)
                return message.message(body='```{}```'.format(', '.join(buildsList)))
            else:
                return message.message(body='User `{}` has no builds!'.format(message_in.author))
        elif len(argsList) == 1:
            if os.path.isfile('cache/build_{}_{}.txt'.format(message_in.author, argsList[0])):
                with open('cache/build_{}_{}.txt'.format(message_in.author, argsList[0])) as f:
                    return message.message(body='```{}```'.format(f.read()))

    if message_in.command == 'addbuild':
        argsList = message_in.body[1:].split(' ', 1)
        if argsList[0] == '':
            return message.message(body='\!addbuild [buildname] [build parts]')
        print(argsList)
        if len(argsList) != 2:
            return message.message(body='\!addbuild [buildname] [build parts]')
        else:
            with open('cache/build_{}_{}.txt'.format(message_in.author, argsList[0]), 'w') as f:
                f.write(argsList[1])
            return message.message(body='Build {} added!'.format(argsList[0]))