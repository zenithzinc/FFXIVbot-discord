def getHelpMessage(action):
    if action == "general":
        return """FFXIV-ZnBot 기능 일람 (Ver.beta)
!판매정보 아이템이름, !제작정보 아이템이름, !주사위 M N, !선택 A B C...
!도움말 (기능) 을 입력하시면 기능별로 상세한 도움말을 보실 수 있습니다. (ex: !도움말 주사위)

기재되어있는 회사명·제품명·시스템 이름은 해당 소유자의 상표 또는 등록 상표입니다.
(C) 2010 - 2017 SQUARE ENIX CO. LTD All Rights Reserved. Korea Published by EYEDENTITY MOBILE.
문의: http://twitter.com/FFXIV_ZnBot, http://znzinc.net/ffxiv/znbot, admin@znzinc.net"""

    elif action == "주사위":
        return """!주사위 M N : 최대값 M인 주사위를 N회 굴린 결과를 보여줍니다.
지원 범위 : 0<M<10000, 0<N<100 (N 생략시 N=1, M과 N 생략 시 M=999, N=1)
예: !주사위 6 3 / !주사위 1000 / !주사위 """

    elif action == "선택":
        return """!선택 A B C ... : 뒤에 입력한 리스트들 중 하나를 랜덤하게 골라줍니다.
리스트는 2개 이상 100개 이하의 요소들로 구성되어야 하며, 모든 선택 요소는 띄어쓰기로 구분되어야 합니다.
예: !선택 처치 텔레포 음식 쇠약 """

    elif action == "판매정보":
        return """!판매정보 아이템 이름 : 뒤에 입력한 아이템을 npc로부터 구할 수 있는지 표시합니다.
아이템 이름은 띄어쓰기와 괄호 등을 정확히 입력해야 합니다. (완벽히 일치하지 않으면 검색되지 않습니다.)
예: !판매정보 하이 에테르"""

    elif action == "제작정보":
        return """!판매정보 아이템 이름 : 뒤에 입력한 아이템을 제작하는데 필요한 재료를 보여줍니다.
아이템 이름은 띄어쓰기와 괄호 등을 정확히 입력해야 합니다. (완벽히 일치하지 않으면 검색되지 않습니다.)
예: !제작정보 하이 에테르"""

    else:
        return """도움말 명령어를 잘못 입력하셨습니다. !도움말 만을 입력하면 전체 도움말을 확인할 수 있습니다."""
