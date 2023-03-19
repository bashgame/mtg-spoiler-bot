# import os
import discord
from discord.ext import commands  # , tasks
import aiohttp
import asyncio
from datetime import date


TOKEN = 'YOUR_BOT_TOKEN'
CHANNEL_ID = 123456789012345678  # Replace with your desired channel ID


async def get_latest_sets(session):
    async with session.get('https://api.scryfall.com/sets') as response:
        if response.status == 200:
            data = await response.json()
            return {set_data['code']: set_data['name'] for set_data in data['data']
                    if date.fromisoformat(set_data['released_at']) > date.today()}
        return {}


async def get_new_spoilers(session, set_code):
    flags = '&order=spoiled&unique=prints'
    url = 'https://api.scryfall.com/cards/search?q=e%3A' + set_code + flags
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            return data['data']
        return []


async def post_spoilers(spoilers, bot):
    channel = bot.get_channel(CHANNEL_ID)
    for spoiler in spoilers:
        embed = discord.Embed(
            title=spoiler['name'], url=spoiler['scryfall_uri'],
            description=spoiler['oracle_text'], color=0x3498db
        )
        embed.set_image(url=spoiler['image_uris']['normal'])
        embed.set_footer(text=spoiler['set_name'])
        await channel.send(embed=embed)


def main():
    intents = discord.Intents.default()
    intents.messages = True
    intents.guilds = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.run(TOKEN)

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

        tracked_sets = {}
        already_spoiled = set()

        async with aiohttp.ClientSession() as session:
            while True:
                # Update the tracked sets
                latest_sets = await get_latest_sets(session)
                for set_code, set_name in latest_sets.items():
                    if set_code not in tracked_sets:
                        tracked_sets[set_code] = set_name
                        print(f'Now tracking set {set_name} ({set_code})')

                # Check for new spoilers in each set
                for set_code in tracked_sets.keys():
                    new_spoilers = await get_new_spoilers(session, set_code)
                    new_spoilers = [spoiler for spoiler in new_spoilers if spoiler['id'] not in already_spoiled]

                    if new_spoilers:
                        await post_spoilers(new_spoilers, bot)
                        already_spoiled.update(spoiler['id'] for spoiler in new_spoilers)

                await asyncio.sleep(3600)  # Check for new sets and spoilers every hour
