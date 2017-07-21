# This bot uses python 3.6

# Ver 1.0.0

import json
import os
import time
from datetime import date
from datetime import datetime

import discord

from commands import bot
keyFile = open("./keys.json", "r")
key = json.loads(keyFile.read())
keyFile.close()

file = open("./channels.txt", "r")
tmp = file.readlines()
channel_list = [x.strip() for x in tmp]
file.close()


def inputLogger(message):
    # input : class message of discord.py
    logfile = open(os.path.join("bot log", str(date.today()) + ".log"), mode="a", newline="\r\n")
    logfile.write("[" + str(time.strftime("%H:%M:%S")) + " " + message.server.name + "#"
                  + message.channel.name + " " + str(message.author) + "]" + message.content + "\n")
    logfile.close()


def noticeLogger(content):
    # input : normal string
    logfile = open("./notice_log.log", mode="a", newline="\r\n")
    logfile.write("[" + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ", sent to " + str(len(channel_list)) + " channels]"
                  + content + "\n")
    logfile.close()


def addToList(ID):
    global channel_list

    channel_list.append(ID)
    listFile = open("./channels.txt", "a")
    listFile.write(ID + "\n")


def deleteFromList(IDs):
    global channel_list

    for ID in IDs:
        channel_list.remove(ID)
    listFile = open("./channels.txt", "w")
    for item in channel_list:
        listFile.write("%s\n" % item)
    listFile.close()


def isInList(ID):
    global channel_list

    try:
        channel_list.index(ID)
        return True
    except:
        return False


botCommands = ["!주사위", "!선택", "!도움말", "!제작정보", "!판매정보"]
adminCommands = ["!공지전송"]


@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='ff14.tar.to'))
    now = datetime.now()
    timestr = str(now)
    print("Discord bot logged in as " + bot.user.name + "(" + bot.user.id + ") at " + timestr)
    print("------------")


@bot.event
async def on_message(message):
    try:
        if message.author == bot.user:
            inputLogger(message)
            return
        cmd = message.content.split(" ")[0]
        if cmd in botCommands:
            if not isInList(message.channel.id):
                addToList(message.channel.id)
            inputLogger(message)
            await bot.process_commands(message)
            return
        if cmd in adminCommands and message.author.id == key["admin"]:
            inputLogger(message)
            await bot.process_commands(message)

    except:
        logfile = open(os.path.join("bot log", str(date.today()) + ".log"), mode="a", newline="\r\n")
        logfile.write("[" + str(time.strftime("%H:%M:%S")) + " ERROR OCCURED HANDLING UPPER MESSAGE.\n")
        logfile.close()


@bot.command(name="공지전송", pass_context=True)
async def sendnotice(ctx, *args):
    global channel_list
    del_list = []
    content = " ".join(args)
    for channel in channel_list:
        try:
            await bot.send_message(discord.Object(channel), "*[관리자 공지] " + content + "*")
        except:
            del_list.append(channel)
    if not len(del_list) == 0:
        deleteFromList(del_list)

    noticeLogger(content)


if not os.path.exists("./bot log"):
    os.makedirs("./bot log")
print("Starting FFXIV-ZnBot...")
while(1):
    try:
        bot.run(key["bot_token"])
    except:
        now = datetime.today()
        print("Bot connection error at " + str(now) + ", Reconnecting in 10 seconds...")
        time.sleep(10)
