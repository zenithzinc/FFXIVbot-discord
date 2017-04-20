# This bot uses python 3.6

# Ver 0.9.0

import json
import os
import time
from datetime import date

import discord

from commands import bot
keyFile = open("./keys.json", "r")
key = json.loads(keyFile.read())
keyFile.close()

botCommands = ["!주사위", "!선택", "!도움말", "!제작정보", "!판매정보"]


def inputLogger(message):
    # input : class message of discord.py
    logfile = open(os.path.join("bot log", str(date.today()) + ".log"), mode="a", newline="\r\n")
    logfile.write("[" + str(time.strftime("%H:%M:%S")) + " " + message.server.name + "#"
                  + message.channel.name + " " + str(message.author) + "]" + message.content + "\n")
    logfile.close()


@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='FINAL FANTASY XIV'))
    print("Discord bot logged in as " + bot.user.name + "(" + bot.user.id + ")")
    print("------------")

async def serverRegister():
    pass


@bot.event
async def on_message(message):
    try:
        if message.author.bot:
            inputLogger(message)
            return
        cmd = message.content.split(" ")[0]
        if cmd in botCommands:
            inputLogger(message)
            await bot.process_commands(message)
            return

    except:
        logfile = open(os.path.join("bot log", str(date.today()) + ".log"), mode="a", newline="\r\n")
        logfile.write("[" + str(time.strftime("%H:%M:%S")) + " ERROR OCCURED HANDLING UPPER MESSAGE.\n")
        logfile.close()


if not os.path.exists("./bot log"):
    os.makedirs("./bot log")
print("Starting discordbot-ffxiv...")
bot.run(key["bot_token"])
