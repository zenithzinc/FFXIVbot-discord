import random
import json

import requests
from discord.ext import commands

import help

bot = commands.Bot(command_prefix="!", description="FFXIV-ZnBot")

keyFile = open("./keys.json", "r")
key = json.loads(keyFile.read())
keyFile.close()
classmap = {"0": "목수", "1": "대장장이", "2": "갑주제작사", "3": "보석공예가",
          "4": "가죽공예가", "5": "재봉사", "6": "연금술사", "7": "요리사"}


def botFormatter(strings, noLink=True):
    # Supposes that links come in only last line.
    if noLink:
        return "```" + strings + "```"
    else:
        lines = strings.split("\n")
        output = ""
        i = 0
        if len(lines) > 1:
            for line in lines:
                output += line
                i += 1
                if i == len(lines) - 1:
                    break
                output += "\n"
            return "```" + output + "```\n*" + lines[i] + "*"
        else:
            return "*" + lines[0] + "*"


@bot.command(name="주사위", pass_context=True, help="!주사위")
async def dice(ctx, *args):
    limit = 999
    rolls = 1
    errcode = 0
    # 0 = accepted / 1 : too large or small number / 2 : not excepted commands
    try:
        if len(args) == 0:
            pass
        elif len(args) == 1:
            limit = int(args[0])
        elif len(args) == 2:
            limit = int(args[0])
            rolls = int(args[1])
        else:
            errcode = 2
    except:
        errcode = 2

    if not (1 <= limit <= 10000) or not (1 <= rolls <= 100):
        errcode = 1

    if errcode == 0:
        result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
        output = "최대값 %d의 주사위 %d회 결과: %s" % (limit, rolls, result)
    elif errcode == 1:
        output = "!주사위 Error: 지원 범위 밖의 값을 입력하셨습니다. (지원 범위 : 0<M<10000, 0<N<100)"
    else:
        output = "!주사위 Error: 잘못된 형식입니다."

    await bot.send_message(ctx.message.channel, botFormatter(output))


@bot.command(name="선택", pass_context=True, help="!선택")
async def selector(ctx, *args):
    message = ctx.message
    try:
        if len(args) == 0:  # no element
            output = "!선택 Error: 입력된 요소가 없습니다."
        elif len(args) == 1:  # 1 element
            output = "!선택 Error: 입력된 요소가 1개 뿐입니다."
        elif len(args) > 100:  # over 100 element
            output = "!선택 Error: 입력된 요소가 100개를 초과하였습니다."
        else:
            output = "선택 결과: %s" % (args[random.randint(0, len(args) - 1)])
    except:
        output = "!선택 Error: 잘못된 형식입니다."

    await bot.send_message(message.channel, botFormatter(output))


@bot.command(name="판매정보", pass_context=True, help="!판매정보")
async def item_sells(ctx, *args):
    itemName = ""
    output = ""
    errcode = 0
    try:
        itemName = " ".join(args)
    except:
        errcode = -1
        output = "!판매정보 Error: 잘못된 형식입니다."
        await bot.send_message(ctx.message.channel, botFormatter(output, errcode))
        return

    try:
        r = requests.get(key["item_name_search_API"] + itemName)
        jsondict = json.loads(r.text)
        count = 0
        try:
            if jsondict["item"]["name"] == "":
                errcode = 1
        except:
            errcode = 1

        if jsondict["seller"]:
            for npc in jsondict["seller"].keys():
                count += 1
                if count > 5:
                    continue
                output = output + jsondict["seller"][npc]["name"] \
                         + " (" + jsondict["place_names"][jsondict["seller"][npc]["place"]] \
                         + " " + jsondict["seller"][npc]["x"] \
                         + ", " + jsondict["seller"][npc]["y"] + ")\n"
            if count > 5:
                output = output + "...외 " + str(count - 5) + "명의 npc가 " + itemName + " 을(를) 판매하고 있습니다.\n"
        else:
            if not errcode == 0:
                output = "!판매정보 Error: 검색 결과가 없습니다."
            else:
                output = output + itemName + " 을(를) 판매하는 npc가 없습니다.\n"
        if errcode == 0:
            output = output + "자세한 정보 확인하기 " + " http://ff14.tar.to/item/view/?number=" + jsondict["item"]["id"]
    except:
        output = "!판매정보 Error: 처리 중 에러가 발생했습니다. 같은 에러가 반복되는 경우 제보해주세요."
        errcode = 1

    await bot.send_message(ctx.message.channel, botFormatter(output, errcode))


@bot.command(name="제작정보", pass_context=True, help="!판매정보")
async def item_recipe(ctx, *args):
    itemName = ""
    output = ""
    errcode = 0
    try:
        itemName = " ".join(args)
    except:
        errcode = -1
        output = "!제작정보 Error: 잘못된 형식입니다."
        await bot.send_message(ctx.message.channel, botFormatter(output, errcode))
        return

    try:
        r = requests.get(key["item_name_search_API"] + itemName)
        jsondict = json.loads(r.text)
        try:
            if jsondict["item"]["name"] == "":
                errcode = 1
        except:
            errcode = 1

        if jsondict["recipies"]:
            count = 0
            for recipe in jsondict["recipies"]:
                count += 1
                if count > 1:
                    continue
                output = output + "[" + classmap[recipe["job"]] + "] " + itemName + " 제작정보\n"
                for i in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    try:
                        if recipe["material_target%s" % i] == "0":
                            break
                    except:
                        break
                    output = output + jsondict["recipe_items"][recipe["material_target%s" % i]]["name"]\
                                    + " " + recipe["material_amount%s" % i] + "개\n"

                # for crystal, item number should be +2"d to get correct item info.
                # https://ffxiv-data.dlunch.net/parsed/ex/kor_330/craftcrystaltype
                for i in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    try:
                        if recipe["crystal_amount%s" % i] == "0":
                            break
                    except:
                        break
                    ino = str(int(recipe["crystal_target%s" % i]) + 2)
                    output = output + jsondict["recipe_items"][ino]["name"]\
                                    + " " + recipe["crystal_amount%s" % i] + "개\n"
            if count > 1:
                output = output + "\n...외 " + str(count - 1) + "개의 다른 직업으로도 제작할 수 있습니다.\n"
        else:
            if not errcode == 0:
                output = "!제작정보 Error: 검색 결과가 없습니다."
            else:
                output = output + itemName + " 에 대한 제작 정보가 없습니다.\n"
        if errcode == 0:
            output = output + "자세한 정보 확인하기 " + " http://ff14.tar.to/item/view/?number=" + jsondict["item"]["id"]
    except:
        output = "!제작정보 Error: 처리 중 에러가 발생했습니다. 같은 에러가 반복되는 경우 제보해주세요."
        errcode = 1

    await bot.send_message(ctx.message.channel, botFormatter(output, errcode))


@bot.command(name="도움말", pass_context=True, help="!도움말")
async def helpMessage(ctx, *args):
    if len(args) == 0:
        output = help.getHelpMessage("general")
        await bot.send_message(ctx.message.channel, botFormatter(output, False))
        return

    if len(args) == 1:
        output = help.getHelpMessage(args[0])
    else:
        output = help.getHelpMessage("asdf")

    await bot.send_message(ctx.message.channel, botFormatter(output))
