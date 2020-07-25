import random
import json
import traceback

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
        title, result = "지원 범위를 벗어난 숫자입니다.", "크기는 10000 미만, 개수는 100 미만의 자연수로 입력해 주세요."
        return [title, result]
    except IndexError:
        pass
    except Exception as e:
        print(e)
        traceback.print_exc()
        title = "내부 오류가 발생했습니다."
        result = "불편을 드려 죄송합니다."
        return [title, result]
    title = "최대값 %d의 주사위 %d회 결과" % (limit, rolls)
    result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))

    return [title, result]


def selector(args):
    try:
        result = "항목은 2개 이상, 20개 이하로 입력해 주세요."
        if len(args) == 0:  # no element
            title = "입력된 항목이 없습니다."
        elif len(args) == 1:  # 1 element
            title = "입력된 항목이 하나 뿐입니다."
        elif len(args) > 20:  # over 20 element
            title = "입력된 항목이 너무 많습니다."
        else:
            title = "선택 결과"
            result = args[random.randint(0, len(args) - 1)]
    except Exception as e:
        print(e)
        traceback.print_exc()
        title = "내부 오류가 발생했습니다."
        result = "불편을 드려 죄송합니다."

    return [title, result]


def item_sellers(args):
    item_name = str(" ".join(args))
    body, url, imageurl = "", "", ""
    try:
        r = requests.post(key["API_item_name_to_id"], {"name": item_name})
        item_list = json.loads(r.text)
        if not item_list:
            title, body = "{} 의 검색 결과가 없습니다.".format(item_name), "아이템 이름을 잘못 입력하신 건 아닌지 확인해주세요."
            return [title, body, url, imageurl]

        item_name = item_list[0]["label"]
        r = requests.post(key["API_item_detail"], {"id": item_list[0]["id"]})
        item_detail = json.loads(r.text)
        url = "https://ff14.tar.to/item/view/{}".format(item_detail["item"]["id"])
        iconid = int(item_detail["item"]["icon"])
        imageurl = "https://ff14.tar.to/assets/img/icon/{:06d}/{:06d}.tex.png".format(int(iconid / 1000) * 1000, iconid)

        enpc_list = item_detail["enpc"]
        senpc_list = item_detail["senpc"]
        if not enpc_list and not senpc_list:
            title = "{} 을(를) 판매하는 NPC가 없습니다.".format(item_name)
            body = "제작할 수 있는 아이템이라면 !제작 명령어로 검색해보세요."
            return [title, body, url, imageurl]

        enpc_infos = []
        enpc_count = 0
        senpc_infos = []
        senpc_count = 0
        senpc_sliced = False
        enpc_sliced = False

        items = item_detail["items"]

        for senpc in senpc_list:
            if senpc["x"] is None:
                continue
            senpc_count += 1
            if senpc_sliced:
                continue
            if senpc_count > 10:
                senpc_sliced = True
                continue

            location = "하우징 혹은 특수필드" if senpc["x"] == -1 else "{} {}, {}".format(senpc["name"],
                                                                             round(senpc["x"], 1), round(senpc["y"], 1))
            senpc_info = "{}({}/".format(senpc["enpc_name"], location)
            for i in range(1, 4):
                if senpc["target_id{}".format(i)] == 0 or senpc["target_id{}".format(i)] is None:
                    break
                if i != 1:
                    senpc_info += ', '
                senpc_info += items[str(senpc["target_id{}".format(i)])]
                if senpc["target_hq{}".format(i)]:
                    senpc_info += ' HQ'
                if senpc["target_collectivity{}".format(i)] is None:
                    senpc["target_collectivity{}".format(i)] = 0
                if senpc["target_collectivity{}".format(i)] > 0:
                    senpc_info += " 소장 가치 {} 이상".format(senpc["target_collectivity{}".format(i)])
                senpc_info += " {}개".format(senpc["target_quantity{}".format(i)])
            senpc_info += ")"
            senpc_infos.append(senpc_info)

        for enpc in enpc_list:
            if enpc["x"] is None:
                continue
            enpc_count += 1
            if enpc_sliced:
                continue
            if enpc_count + senpc_count > 10 and enpc_count > 5:
                enpc_sliced = True
                continue

            location = "하우징 혹은 특수필드" if enpc["x"] == -1 else "{} {}, {}".format(enpc["placename"],
                                                                               round(enpc["x"], 1), round(enpc["y"], 1))
            enpc_info = "{}({}/{}길)".format(enpc["name"], location, item_detail["item"]["price_a"])
            enpc_infos.append(enpc_info)

        total_list = enpc_infos + senpc_infos
        if len(total_list) > 10:
            total_list = total_list[0:10]
            senpc_sliced = True
        body = "\n".join(total_list)
        if enpc_sliced or senpc_sliced:
            body += " 등"

        title_part = "판매 및 교환" if senpc_count > 0 and enpc_count > 0 else "판매" if senpc_count == 0 else "교환"
        title = "[{}] {} 정보".format(item_name, title_part)

    except Exception as e:
        print(e)
        traceback.print_exc()
        title, body = "내부 오류가 발생했습니다.", "불편을 드려 죄송합니다."
        imageurl = ""
    return [title, body, url, imageurl]


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
                title = itemName + " 에 대한 제작 정보가 없습니다."
                body = "판매 혹은 교환으로 입수할 수 있는 아이템이라면 !판매 명령어로 검색해보세요."
            if len(recipes) != 0:
                url = "http://ff14.tar.to/item/view/" + str(itemList[0]["id"])
        else:
            title, body = itemName + " 의 검색 결과가 없습니다.", "아이템 이름을 잘못 입력하신건 아닌지 확인해주세요."
    except Exception as e:
        print(e)
        traceback.print_exc()
        title, body = "내부 오류가 발생했습니다.", "불편을 드려 죄송합니다."

    return [title, body, url]
