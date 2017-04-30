# ![StarIcon](https://68.media.tumblr.com/avatar_129c75279689_128.png) Starbot - an open source Discord bot

[![TravisIcon](https://avatars.githubusercontent.com/u/6227399?size=100)](https://travis-ci.org/StarbotDiscord/Starbot)|[![ReadthedocsIcon](https://avatars2.githubusercontent.com/u/366329?v=3&s=100)](http://starbot.readthedocs.io/en/latest/)|[![JiraIcon](https://www.clearvision-cm.com/wp-content/themes/clearvision_v3/img/menu/atlassian.png)](https://sydstudios.atlassian.net/projects/SB/issues/)|[![DiscordIcon](https://screenshots.en.sftcdn.net/en/scrn/69730000/69730439/discord-01-100x100.png)](https://discord.gg/JEYSJxn)
:-----:|:-----:|:-----:|:-----:
[![Build Status](https://travis-ci.org/StarbotDiscord/Starbot.svg?branch=master)](https://travis-ci.org/StarbotDiscord/Starbot)|[![Doc Status](https://readthedocs.org/projects/starbot/badge/?version=latest)](http://starbot.readthedocs.io/en/latest/)|[Jira Tracker](https://sydstudios.atlassian.net/projects/SB/issues/)|[![DiscordIcon](https://discordapp.com/api/guilds/302626068848705536/widget.png)](https://discord.gg/JEYSJxn)

## What's Starbot about?
Starbot is a plugin based bot for Discord. You should never have to edit the core of the bot or other plugins to add your awesome features! Due to the nature of the plugin system you can choose exactly what features the bot has.

## How do I install Starbot?
Installing Starbot is pretty simple.

1. Use your package manager (or otherwise obtain) a copy of Python >=3.5, Git and Pip for Python 3
2. `git clone https://github.com/1byte2bytes/Starbot.git`
3. `pip install discord.py pluginbase psutil pyparsing pyspeedtest tqdm`
4. Git a bot token from the [Discord Developers page](https://discordapp.com/developers/applications/me)
5. Paste the token for the bot user into a file called `token.txt` in the folder with the bots code
6. `./run.sh` to start the bot!

## I'd like to contribute!
Contributing to Starbot is always welcome and pretty simple.
If you encounter a bug, have a suggestion, etc then visit the Jira tracker using the link above and write out a ticket.
If you want to write a plugin, check out the documentation above.
If you'd like to contribute to the core of the bot or have your plugin merged into the main bot, create a fork on GitHub and then pull request when you've made your changes.
