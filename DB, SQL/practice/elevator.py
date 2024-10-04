def goDownfloor(now, target):
    for floor in range(now, target-1, -1):
        print(f'현재 층은{floor}입니다.')
    print(f'{target}층에 도착하였습니다. 안녕히 가세요.')


def goUpfloor(now, target):
    for floor in range(now, target+1):
        print(f'현재 층은{floor}입니다.')
    print(f'{target}층에 도착하였습니다. 안녕히 가세요.')


while True:
    inputLocation = int(input('가고자 하는 층 입력: '))
    nowLocation = int(input('현재 위치 입력: '))

    if ((inputLocation == nowLocation) or (inputLocation < 1) or (6 < inputLocation)):
        print("다른 층(1~6)을 눌러주세요.")
    else:
        if(nowLocation > inputLocation):
            goDownfloor(nowLocation, inputLocation)
            break
        else:
            goUpfloor(nowLocation, inputLocation)
            break