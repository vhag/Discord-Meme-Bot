from ast import arg
import discord
from discord.ext import commands
import requests
import urllib
from os import getenv
from dotenv import load_dotenv

load_dotenv(".env")
username = getenv("IMGFLIP_API_USERNAME")
password = getenv("IMGFLIP_API_PASSWORD")
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 \
    Safari/537.36'
data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']

class MemeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="meme")
    async def meme_cmd(self, ctx, *args):
        if len(args) < 2:
            await ctx.send('Nämen! Man måste skriva "meme [siffra] [ord]')
            return 0
        if len(args) > 5:
            await ctx.send("För många ord! Max fyra.")
            return 0
        if not int(args[0]):
            await ctx.send("Du måste börja med en siffra.")
            return 0            
        args = list(args)
        id = int(args[0])
        number_of_words = len(args)-1
        if number_of_words == 4:
            pass
        elif number_of_words == 3:
            args.extend([""])
        elif number_of_words == 2:
            args.extend(["", ""])
        elif number_of_words == 1:
            args.extend(["", "", ""])
            
        images = [{'name': image['name'], 'url': image['url'],'id': image['id']} for image in data]

        url = 'https://api.imgflip.com/caption_image'
        params = {
            'username': username,
            'password': password,
            'template_id': images[id-1]['id'],
            'boxes[0][text]': args[1],
            'boxes[1][text]': args[2],
            'boxes[2][text]': args[3],
            'boxes[3][text]': args[4]
        }
        response = requests.request('POST', url, params=params).json()
        try:
            link = response['data']['url']
        except KeyError:
            print(response)
            return 0
        await ctx.send(str(link))

    @commands.command(name="list")
    async def list_cmd(self, ctx, arg0=1):
        try:
            arg0 = int(arg0)
        except ValueError:
            await ctx.send("Siffror, grabben.")
            return 0
        
        page_size = 20
        number_of_pages = int(100/page_size)
        if arg0 > number_of_pages or arg0 < 1:
            await ctx.send(f"Det finns {number_of_pages} sidor, nåt annat vore absurt.")
            return 0
            
        slice_start = arg0 * page_size-page_size
        slice_end = page_size * int(arg0)
        new_data = data[slice_start:slice_end]
        tupled_list = [(i + page_size * (arg0-1), image['name']) for i, image in enumerate(new_data)]

        list_of_memes = f"(Page {arg0} of {number_of_pages})\n"
        for img in tupled_list:
            list_of_memes += f"{img[0]+1}: {img[1]}\n"
        await ctx.send(list_of_memes)

def setup(bot):
    bot.add_cog(MemeCog(bot))