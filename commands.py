import random
import json

import requests
from discord.ext import commands
import discord


keyFile = open("./keys.json", "r")
key = json.loads(keyFile.read())
keyFile.close()
classmap = {0: "목수", 1: "대장장이", 2: "갑주제작사", 3: "보석공예가", 4: "가죽공예가", 5: "재봉사", 6: "연금술사", 7: "요리사"}


def dice(args):
    limit, rolls = 999, 1
    errcode = 0
    # 0 = accepted / 1 : too large or small number / 2 : not excepted commands
    try:
        if len(args) == 0:
            pass
        elif len(args) == 1:
            limit = int(args[0])
        elif len(args) == 2:
            limit, rolls = int(args[0]), int(args[1])
        else:
            errcode = 2
    except:
        errcode = 2

    if not (1 <= limit <= 10000) or not (1 <= rolls <= 100):
        errcode = 1
    if errcode == 0:
        title = "최대값 %d의 주사위 %d회 결과" % (limit, rolls)
        result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
    elif errcode == 1:
        title, result  = "주사위 Error", "지원 범위 밖의 값을 입력하셨습니다. (지원 범위 : 0<M<10000, 0<N<100)"
    else:
        title, result = "주사위 Error", "잘못된 형식입니다."

    return [title, result]


def selector(args):
    title = "선택 Error"
    try:
        if len(args) == 0:  # no element
            result = "입력된 요소가 없습니다."
        elif len(args) == 1:  # 1 element
            result = "입력된 요소가 1개 뿐입니다."
        elif len(args) > 20:  # over 20 element
            result = "입력된 요소가 20개를 초과하여 처리할 수 없습니다."
        else:
            title = "선택 결과"
            result = args[random.randint(0, len(args) - 1)]
    except:
        output = "잘못된 형식입니다."

    return [title, result]


def item_sellers(args):
    itemName, output, url = "", "", ""
    errcode = 0
    try:
        itemName = " ".join(args)
    except:
        title, output = "판매정보 Error", "잘못된 형식입니다."
        return [[title, output, url]]
    try:
        r = requests.post(key["API_item_name_to_id"], {"name": itemName})
        itemlist = json.loads(r.text)
        itemName = itemlist[0]["label"]
        r = requests.post(key["API_item_detail"], {"id": itemlist[0]["id"]})
        sellerlist = json.loads(r.text)["enpc"]
        count = 0
        title = "[" + itemName + "] 판매 정보"
        for npc in sellerlist:
            count += 1
            if count > 5:
                continue
            else:
                output = output + npc["name"] + " (" + npc["placename"] + " "\
                         + str(round(npc["x"], 1)) + ", " + str(round(npc["y"], 1)) + ")\n"
        if count > 5:
            output = output + "...외 " + str(count - 2) + "명의 npc가 " + itemName + " 을(를) 판매하고 있습니다."
        elif count == 0:
            output = itemName + " 을(를) 판매하는 npc가 없습니다."
        if errcode == 0:
            url = " http://ff14.tar.to/item/view/" + str(itemlist[0]["id"])
    except Exception as e:
        print(e)
        title, output = "판매정보 Error", "처리 중 에러가 발생했습니다. 같은 에러가 반복되는 경우 제보해주세요."
    return [title, output, url]


def item_recipe(args):
    itemName, output, url = "", "", ""
    errcode = 0
    try:
        itemName = " ".join(args)
    except:
        title, output = "제작정보 Error", "잘못된 형식입니다."
        return [[title, output, url]]
    try:
        r = requests.post(key["API_item_name_to_id"], {"name": itemName})
        itemlist = json.loads(r.text)
        itemName = itemlist[0]["label"]
        r = requests.post(key["API_item_detail"], {"id": itemlist[0]["id"]})
        details = json.loads(r.text)
        recipes = details["recipes"]
        items = details["items"]
        count = 0
        for recipe in recipes:
            count += 1
            if count > 1:
                continue
            title = "[" + itemName + "] 제작정보 (" + classmap[recipe["job"]] + ")"
            for i in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                try:
                    if recipe["material_target%s" % i] == 0:
                        break
                except:
                    break
                output = output + items[str(recipe["material_target%s" % i])] \
                         + " " + str(recipe["material_amount%s" % i]) + "개\n"

            for i in ["1", "2", "3"]:
                try:
                    if recipe["crystal_amount%s" % i] == 0:
                        break
                except:
                    break
                output = output + items[str(recipe["crystal_target%s" % i])] \
                         + " " + str(recipe["crystal_amount%s" % i]) + "개\n"
        if count > 1:
            output = output + "(총 " + str(count) + "개의 직업으로 제작 가능)"
        elif count == 0:
            title, output = "[" + itemName + "] 제작정보", itemName + " 에 대한 제작 정보가 없습니다."
        if errcode == 0:
            url = "http://ff14.tar.to/item/view/" + str(itemlist[0]["id"])
    except Exception as e:
        print(e)
        title, output = "제작정보 Error", "처리 중 에러가 발생했습니다. 같은 에러가 반복되는 경우 제보해주세요."

    return [title, output, url]

