from glob import glob
from pathlib import Path

import discord
import datetime
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

import os
load_dotenv(".env")


class Bot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./Bot/cogs/*.py")]
        super().__init__(command_prefix=self.prefix, case_insensitive=True, intents=Intents.all())

        self.startup = False


    def setup(self):
        print("Cogs are Loading...")

        for cog in self._cogs:
            self.load_extension(f"Bot.cogs.{cog}")
            print(f" Loaded `{cog}` cog.")

        print("All Cogs are Loaded.")

    

    def run(self):
        self.setup()

        TOKEN = os.getenv("BOTTOKEN")

        print("Bot is starting...")
        super().run(TOKEN, reconnect=True)


    async def on_connect(self):
        print(f"Connected to Discord (latency: {self.latency*1000:,.0f} ms).")
        if self.startup is False:
            #You can put code in here to only run once. On start only
            self.startup = True
        
        activity = discord.Activity(
            name=f'Botten startar, vänta lite...',
            type=discord.ActivityType.playing)
        await self.change_presence(status=discord.Status.dnd, activity=activity)
   

    async def on_resumed(self):
        print("Bot resumed")
        
    async def on_disconnect(self):
        print("Bot disconnected")
    async def on_ready(self):
        print("Bot is ready!")
        activity = discord.Activity(
            name=f"{os.getenv('STATUS')}",
            type=discord.ActivityType.watching)
        await self.change_presence(status=discord.Status.online, activity=activity)

    async def prefix(self, bot, message):
        return commands.when_mentioned_or(f"{os.getenv('PREFIX')}")(bot, message)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)
        await self.invoke(ctx) 

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)