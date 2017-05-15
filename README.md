<h2 align="center"><a href="http://dm29.deviantart.com/art/I-ve-Got-a-New-Wand-620381797"><img src="http://pre12.deviantart.net/b15e/th/pre/f/2016/192/c/3/i_ve_got_a_new_wand__by_dm29-da9cxnp.png" width="128px"></a> Starbot - an open source Discord bot<br>
<a href="https://travis-ci.org/StarbotDiscord/Starbot"><img src="https://img.shields.io/travis/StarbotDiscord/Starbot.svg?style=flat-square"/></a>
<a href="http://starbot.readthedocs.io/en/latest/"><img src="https://readthedocs.org/projects/starbot/badge/?version=latest&style=flat-square"/></a>
<a href="https://sydstudios.atlassian.net/projects/SB/issues/"><img src="https://img.shields.io/badge/jira-starbot-brightgreen.svg?style=flat-square"/></a>
<a href="https://discord.gg/JEYSJxn"><img src="https://img.shields.io/discord/302626068848705536.svg?style=flat-square" /></a></h2>

## What's Starbot about?
Starbot is a plugin based bot for Discord. You should never have to edit the core of the bot or other plugins to add your awesome features! Due to the nature of the plugin system you can choose exactly what features the bot has.

## How do I install Starbot?
Installing Starbot is pretty simple.

1. Use your package manager (or otherwise obtain) a copy of Python >=3.5, Git and Pip for Python 3
2. `git clone https://github.com/StarbotDiscord/Starbot.git`
3. `pip install discord.py pluginbase psutil pyparsing pyspeedtest tqdm`
4. Git a bot token from the [Discord Developers page](https://discordapp.com/developers/applications/me)
5. Paste the token for the bot user into a file called `token.txt` in the folder with the bots code
6. `./run.sh` to start the bot!

## I'd like to contribute!
Contributing to Starbot is always welcome and pretty simple.
If you encounter a bug, have a suggestion, etc then visit the Jira tracker using the link above and write out a ticket.
If you want to write a plugin, check out the documentation above.
If you'd like to contribute to the core of the bot or have your plugin merged into the main bot, create a fork on GitHub and then pull request when you've made your changes.
