import random
import json

import requests

keyFile = open("./keys.json", "r")
key = json.loads(keyFile.read())
keyFile.close()
classmap = {0: "목수", 1: "대장장이", 2: "갑주제작사", 3: "보석공예가", 4: "가죽공예가", 5: "재봉사", 6: "연금술사", 7: "요리사"}


def dice(args):
    limit, rolls = 999, 1
    try:
        limit = int(args[0])
        if not 1 <= limit <= 10000:
            raise ValueError
        rolls = int(args[1])
        if not 1 <= rolls <= 100:
            raise ValueError
    except ValueError:
        title, result = "주사위 Error", "잘못된 형식입니다.(지원 범위 : 0<크기<=10000, 0<개수<=100)"
        return [[title, result]]
    except IndexError:
        pass
    title = "최대값 %d의 주사위 %d회 결과" % (limit, rolls)
    result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))

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
        result = "잘못된 형식입니다."

    return [title, result]


def item_sellers(args):
    itemName = str(" ".join(args))
    body, url = "", ""
    try:
        r = requests.post(key["API_item_name_to_id"], {"name": itemName})
        itemList = json.loads(r.text)
        if not itemList == []:
            itemName = itemList[0]["label"]
            r = requests.post(key["API_item_detail"], {"id": itemList[0]["id"]})
            sellerList = json.loads(r.text)["enpc"]
            title = "[" + itemName + "] 판매 정보"
            no_of_sellers = len(sellerList)
            if no_of_sellers == 0:
                body = itemName + " 을(를) 판매하는 npc가 없습니다."
            else:
                count = 0
                url = " http://ff14.tar.to/item/view/" + str(itemList[0]["id"])
                for npc in sellerList:
                    count += 1
                    if count <= 5:
                        body = body + npc["name"] + " (" + npc["placename"] + " " \
                               + str(round(npc["x"], 1)) + ", " + str(round(npc["y"], 1)) + ")\n"
                    else:
                        body = body + "...외 " + str(no_of_sellers - 5) + "명의 npc가 " + itemName + " 을(를) 판매하고 있습니다."
                        break
        else:
            title, body = "판매정보 Error", itemName + " 의 검색 결과가 없습니다."
    except Exception as e:
        print(e)
        title, body = "판매정보 Error", "처리 중 에러가 발생했습니다. 같은 에러가 반복되는 경우 제보해주세요."
    return [title, body, url]


def item_recipe(args):
    itemName = str(" ".join(args))
    body, url = "", ""
    try:
        r = requests.post(key["API_item_name_to_id"], {"name": itemName})
        itemList = json.loads(r.text)
        if not itemList == []:
            itemName = itemList[0]["label"]
            r = requests.post(key["API_item_detail"], {"id": itemList[0]["id"]})
            details = json.loads(r.text)
            recipes = details["recipes"]
            items = details["items"]
            recipe = recipes[0]
            title = "[" + itemName + "] 제작정보 (" + classmap[recipe["job"]] + ")"
            for i in range(1, 10):
                try:
                    if recipe["material_target%s" % str(i)] == 0:
                        break
                except:
                    break
                body = body + items[str(recipe["material_target%s" % str(i)])] \
                       + " " + str(recipe["material_amount%s" % str(i)]) + "개\n"
            for i in range(1, 4):
                try:
                    if recipe["crystal_amount%s" % str(i)] == 0:
                        break
                except:
                    break
                body = body + items[str(recipe["crystal_target%s" % str(i)])] \
                       + " " + str(recipe["crystal_amount%s" % str(i)]) + "개\n"
            if len(recipes) > 1:
                body = body + "(총 " + str(len(recipes)) + "개의 직업으로 제작 가능)"
            elif len(recipes) == 0:
                title, body = "[" + itemName + "] 제작정보", itemName + " 에 대한 제작 정보가 없습니다."
            if len(recipes) != 0:
                url = "http://ff14.tar.to/item/view/" + str(itemList[0]["id"])
        else:
            title, body = "제작정보 Error", itemName + " 의 검색 결과가 없습니다."
    except Exception as e:
        print(e)
        title, body = "제작정보 Error", "처리 중 에러가 발생했습니다. 같은 에러가 반복되는 경우 제보해주세요."

    return [title, body, url]
