import discord
import asyncio
import git

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!info'):
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        await client.send_message(message.channel, '```Project StarBot v0.0.1-{}\r\nDeveloped by CorpNewt and Sydney Erickson```'.format(sha[:5]))

client.run('Mjg2NjUxNTk3NDIzOTAyNzIw.C5j0sw.qF968us3onhFSyjOgnv6-fr4_SU')