import json
import datetime
import asyncio
import requests
from discord.ext import commands

from core.cog import Cog_Extension

class Tools(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = 0

        async def time_task():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                with open('messages.json', 'r', encoding='utf8') as f:
                    messages = json.load(f)
                now = datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
                # print(now)
                for message in messages:
                    if message['time'] == now:
                        channel = self.bot.get_channel(int(message['channel_id']))
                        url = f'https://discord.com/api/v9/channels/{message["channel_id"]}/messages'
                        data = {'content': message['message']}
                        with open('config.json', 'r') as f:
                            user_token = json.load(f)['user_token']
                        headers = {'authorization': user_token}
                        r = requests.post(url, data=data, headers=headers)
                        if r.status_code == 200:
                            print(f'Sent {message["message"]} to {message["channel_id"]} successfully')
                        else:
                            print(f'Failed to send {message["message"]} to {message["channel_id"]}')
                        with open('messages.json', 'r', encoding='utf8') as f:
                            _messages = json.load(f)
                        _id = message['id']
                        _messages = [i for i in _messages if i['id'] != _id]
                        with open('messages.json', 'w', encoding='utf8') as f:
                            json.dump(_messages, f, indent=4, ensure_ascii=False)
                        
                await asyncio.sleep(.7)
                
        self.bot.loop.create_task(time_task())
    
    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def set_token(self, ctx: commands.Context, token):
        with open('config.json', 'r') as f:
            config = json.load(f)
        config['bot_token'] = token
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        await ctx.send('Token set successfully')

    @commands.command()
    async def set_message_prefix(self, ctx: commands.Context, *message_prefix):
        with open('config.json', 'r') as f:
            config = json.load(f)
        config['message_prefix'] = ' '.join(message_prefix)
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        await ctx.send('Message prefix set successfully')

    @commands.command()
    async def send(self, ctx: commands.Context, time, channel_id, *message):
        with open('config.json', 'r') as f:
            message_prefix = json.load(f)['message_prefix']
        with open('messages.json', 'r', encoding='utf8') as f:
            messages = json.load(f)
        messages.append({
            'id': self.id,
            'time': time,
            'channel_id': channel_id,
            'message': message_prefix + ' '.join(message)
        })
        with open('messages.json', 'w', encoding='utf8') as f:
            json.dump(messages, f, indent=4, ensure_ascii=False)
        await ctx.send(f'Message scheduled successfully\nMessage ID: {self.id}')
        self.id += 1

async def setup(bot: commands.Bot):
    await bot.add_cog(Tools(bot))