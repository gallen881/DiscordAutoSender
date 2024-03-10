import os
import asyncio
import json
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='-', intents=discord.Intents.all())

async def main():
    @bot.event
    async def on_ready():
        await bot.change_presence(status=discord.Status.online)
        print('Bot is ready')

    @bot.command()
    @commands.is_owner()
    async def load(ctx: commands.Context, extension):
        await bot.load_extension(f'extensions.{extension}')
        await ctx.send(f'Loaded {extension} successfully')
        print(f'Loaded {extension} successfully')

    @bot.command(aliases=['ul'])
    @commands.is_owner()
    async def unload(ctx: commands.Context, extension):
        await bot.unload_extension(f'extensions.{extension}')
        await ctx.send(f'Unloaded {extension} successfully')
        print(f'Unloaded {extension} successfully')

    @bot.command(aliases=['rl'])
    @commands.is_owner()
    async def reload(ctx: commands.Context, extension):
        await bot.reload_extension(f'extensions.{extension}')
        await ctx.send(f'Reloaded {extension} successfully')
        print(f'Reloaded {extension} successfully')

    async with bot:
        for file in os.listdir('./extensions'):
            if file.endswith('.py'): await bot.load_extension(f'extensions.{file[:-3]}')
        with open('config.json', 'r') as f:
            config = json.load(f)
        await bot.start(config['bot_token'])

asyncio.run(main())