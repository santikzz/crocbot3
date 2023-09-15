import discord
from discord.ext import tasks
import json
import httpx
import os
import random
# import scraper
# import math

import twitch
import piratebay

DISCORD_OWNER_ID = 221989916131721216
DEV_CHANNEL = 912904428112195624
CROC_CHANNEL = 879174924277780500

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    print("Ready!")
    await client.change_presence(activity=discord.Game("The fucking croc"))
    check_stream_cron.start()
    pb_check_cron.start()

@tasks.loop(minutes=60)
async def check_stream_cron():
    fstreamers = open("streamers.json", "r")
    streamers = json.loads(fstreamers.read())

    for streamer in streamers:
        
        if twitch.check_stream_status(streamer):
            if not streamers[streamer]["is_live"]:
                message = f'**{streamer}** is now live on Twitch!'
                user = client.get_user(DISCORD_OWNER_ID)
                await user.send(message)
                streamers[streamer]["is_live"] = True;
        else:
            streamers[streamer]["is_live"] = False;

    fstreamers = open("streamers.json", "w")
    fstreamers.write(json.dumps(streamers))

@tasks.loop(hours=12)
async def pb_check_cron():

    pb = piratebay.pb_check()
    if pb:
        user = client.get_user(DISCORD_OWNER_ID)
        await user.send(f"\"{pb['name']}\" -> https://tpb.re/description.php?id={pb['id']}")

@client.event
async def on_message(message):

    if message.author.bot:
        return

    if message.content == "croc random":
        files = os.listdir("/var/www/html/croc/")
        file = random.choice(files)
        # !!!! QRAND NOW THROTTLED TO 1 REQ/MIN !!!!
        # get and parse quantum random number from qrng
        # qint = httpx.get("https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint16").text
        # qint = int(json.loads(qint)["data"][0])
        # qint = math.ceil(qint/65535*len(files))
        # select image index
        # file = files[qint] 
        embed = discord.Embed()
        embed.set_image(url=f"http://181.29.104.6/croc/{file}")
        await message.channel.send(embed=embed)

    if message.content.startswith("!confesion "):
        channel = client.get_channel(1084622987568885761)
        await channel.send(f"Confesion anonima: {message.content[11:]}")

    # PATROCO_ID = 293752876797263872
    # if (message.author.id == PATROCO_ID and (message.mentions or message.role_mentions)):
    #     await message.delete()
    #     await message.channel.send(":rage:")

client.run("")