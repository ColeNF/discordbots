import discord
from discord.ext import commands 
from bin.scores import Scores
import logging as log

INTENTS = discord.Intents.all()

class EpicDiscordBot(commands.Bot):
    def __init__(self, data_path:str):
        super(EpicDiscordBot, self).__init__(command_prefix='!', intents=INTENTS)
        log.info(f'Registering cogs')
        self.add_cog(Scores(self, data_path))

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')
    
    async def get_connected_voice(self, channel_id):
        chnl = await self.fetch_channel(channel_id)
        ids = chnl.voice_states.keys() 

        members = []
        for id in ids:
            usr = await self.fetch_user(id)
            members.append(usr.display_name)
        return members

async def test_loop(client:EpicDiscordBot):
    while True:
        input('Press enter to run get_connected_voice')

        print(await client.get_connected_voice(740393371021082793))

if __name__ == '__main__':
    from prod import conf
    import asyncio
    import threading
    
    DISCORD_TOKEN = conf['discord']['bot_token'].get()
    DATA_PATH = conf['discord']['slur_data'].get(str)
    
    client = EpicDiscordBot(DATA_PATH)
    loop = asyncio.get_event_loop()
    loop.create_task(client.start(DISCORD_TOKEN))
    threading.Thread(target=loop.run_forever, daemon=True).start()
    # loop.run_forever()

    asyncio.run(test_loop(client))