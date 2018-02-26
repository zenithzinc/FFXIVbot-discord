# This bot uses python 3.6
# Encoding: UTF-8

import json
import os
import time
from datetime import date
from datetime import datetime
import help

import discord
from discord.ext import commands as discord_commands

import commands
import twitter
with open("./keys.json", "r") as keyFile, open("./channels.txt", "r") as channelFile:
    key = json.loads(keyFile.read())
    tmp = channelFile.readlines()
    channel_list = [x.strip() for x in tmp]


bot = discord_commands.Bot(command_prefix="!", description="FFXIV-ZnBot")


async def send_as_embed(channel, title, description, url="", message=""):
    em = discord.Embed(title=title, description=description, url=url, colour=0x787978)
    await bot.send_message(channel, message, embed=em)


def input_logger(message):
    # input : class message of discord.py
    with open(os.path.join("bot log", str(date.today()) + ".log"), mode="a", newline="\r\n") as logfile:
        logfile.write("[" + str(time.strftime("%H:%M:%S")) + " " + message.server.name + "#"
                      + message.channel.name + " " + str(message.author) + "]" + message.content + "\n")


botCommands = ["!주사위", "!선택", "!도움말", "!제작정보", "!제작검색", "!제작", "!판매정보", "!판매검색", "!판매"]
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
            input_logger(message)
            return
        cmd = message.content.split(" ")[0]
        if cmd in botCommands:
            if not is_in_list(message.channel.id):
                add_to_list(message.channel.id)
            input_logger(message)
            await bot.process_commands(message)
            return
        if cmd in adminCommands and message.author.id == key["admin"]:
            input_logger(message)
            await bot.process_commands(message)

    except:
        with open(os.path.join("bot log", str(date.today()) + ".log"), mode="a", newline="\r\n") as logFile:
            logFile.write("[" + str(time.strftime("%H:%M:%S")) + " ERROR OCCURED HANDLING UPPER MESSAGE.\n")


@bot.command(name="주사위", pass_context=True, help="!주사위")
async def bot_dice(ctx, *args):
    returned = commands.dice(args)
    await send_as_embed(ctx.message.channel, returned[0], returned[1])


@bot.command(name="선택", pass_context=True, help="!선택")
async def bot_selector(ctx, *args):
    returned = commands.selector(args)
    await send_as_embed(ctx.message.channel, returned[0], returned[1])


@bot.command(name="판매정보", pass_context=True, help="!판매정보", aliases=["판매검색", "판매"])
async def bot_item_sellers(ctx, *args):
    returned = commands.item_sellers(args)
    await send_as_embed(ctx.message.channel, returned[0], returned[1], url=returned[2])


@bot.command(name="제작정보", pass_context=True, help="!제작정보", aliases=["제작검색", "제작"])
async def bot_item_recipe(ctx, *args):
    returned = commands.item_recipe(args)
    await send_as_embed(ctx.message.channel, returned[0], returned[1], url=returned[2])


@bot.command(name="도움말", pass_context=True, help="!도움말")
async def help_message(ctx, *args):
    if len(args) == 0:
        output = help.getHelpMessage("general")
    elif len(args) == 1:
        output = help.getHelpMessage(args[0])
    else:
        output = help.getHelpMessage("asdf")

    await send_as_embed(ctx.message.channel, output[0], output[1])


# Admin commands


def notice_logger(content):
    # input : normal string
    with open("./notice_log.log", mode="a", newline="\r\n") as logfile:
        logfile.write("[" + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ", sent to "
                      + str(len(channel_list)) + " channels]" + content + "\n")


def add_to_list(ID):
    global channel_list
    channel_list.append(ID)
    with open("./channels.txt", "a") as listFile:
        listFile.write(ID + "\n")


def delete_from_list(IDs):
    global channel_list
    for ID in IDs:
        channel_list.remove(ID)
    with open("./channels.txt","w") as listFile:
        for item in channel_list:
            listFile.write("%s\n" % item)


def is_in_list(ID):
    global channel_list
    try:
        channel_list.index(ID)
        return True
    except:
        return False


@bot.command(name="공지전송", pass_context=True)
async def send_notice(ctx, *args):
    global channel_list
    del_list = []
    content = " ".join(args)
    for channel in channel_list:
        try:
            await bot.send_message(discord.Object(channel), "*[관리자 공지] " + content + "*")
        except:
            del_list.append(channel)
    if not len(del_list) == 0:
        delete_from_list(del_list)

    notice_logger(content)


# Bot running part


if not os.path.exists("./bot log"):
    os.makedirs("./bot log")
print("Starting FFXIV-ZnBot...")
try:
    bot.run(key["bot_token"])
except Exception as e:
    now = datetime.today()
    try:
        twitter.tweet_now(str(now) + "경 장애가 발생하여 봇이 잠시 중단되었습니다. 복구될때까지 잠시만 기다려 주십시오.")
    except:
        pass
    print("Bot died at" + str(now) + "with error: " + str(e))