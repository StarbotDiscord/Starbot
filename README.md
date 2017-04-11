# Starbot - An Open-Source Discord Bot [![Build Status](https://travis-ci.org/StarbotDiscord/Starbot.svg?branch=master)](https://travis-ci.org/StarbotDiscord/Starbot) [![Doc Status](http://starbot.readthedocs.io/en/latest/?badge=latest)](http://starbot.readthedocs.io/en/latest/)

## Project Overview

Welcome to the Starbot project! This project is intended as a complete overhaul of [CorpNewt's CorpBot.py](https://github.com/corpnewt/CorpBot.py) project. The bot includes many features, silly and useful. A list of commands will be posted soon(tm), since the bot is under very active development.

## Why should I use this bot?

Most people probably won't find the bot too useful in it's current state. It's in the very early stages and is composed of mostly developer and debug commands. Your welcome to run it if you'd like a toy to mess with though.

## I've encountered an issue!

If you've found a problem with Starbot, please report it to the [JIRA](https://sydstudios.atlassian.net/projects/SB/issues/?filter=allopenissues) - it's free to make an account and helps us keep track of the problems in the bot!

## How can I contribute?

### Documentation

[You may read the docs here](http://starbot.readthedocs.io/en/latest/)

### Making plugins

This is very easy! Go ahead and [take the template and hack it up to your hearts content.](http://starbot.readthedocs.io/en/latest/getstarted.html#a-basic-plugin-text-manipulation) This can be in your own repo, no need to clone the bot. Third party plugins are welcomed, and the bot doesn't need any modifications to run them. Plugins would go into the `plugins` folder.

### Working on the core

If your feeling particularly adventurous you may find working on the core of the bot appealing. This would include all the very core features and APIs. Start by looking through the [JIRA](https://sydstudios.atlassian.net/projects/SB/issues/?filter=allopenissues) for open issues and reading through the [documentation](http://starbot.readthedocs.io/en/latest/).

## Installing and running Starbot

_There may be a build of the [StarBot Runtime](https://github.com/StarbotDiscord/BuildScript) available that works on your system if you're feeling adventurous._

1. Make sure you have Python 3.5 or 3.6 installed, as well as git

2. Run `pip install discord.py pluginbase psutil gitpython pyparsing pyspeedtest requests tqdm` in a terminal session to install the dependancies

3. Run `git clone https://github.com/1byte2bytes/Starbot.git` to copy the code to your local system

4. Run `echo [my token here] > token.txt` to create a file for the bots token

5. Run `./run.sh` to run the bot!

