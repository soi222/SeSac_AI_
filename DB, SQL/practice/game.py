print('### 가위, 바위, 보 게임 ###')
print('삼선승제로 세판 먼저 이기는 사람이 승리!!')
print('------------------------------------')

# 승리 횟수 저장을 위한 변수
win_a = 0
win_b = 0

while win_a < 3 and win_b < 3:
    user_a = input('user1 > 가위, 바위, 보를 입력하세요 : ')
    user_b = input('user2 > 가위, 바위, 보를 입력하세요 : ')

    if user_a == '가위':
        if user_b == '가위':
            print('무승부')
        elif user_b == '바위':
            print('user2 승리')
            win_b += 1
        elif user_b == '보':
            print('user1 승리')
            win_a += 1

        else:
            print('user2 값 오류 ->', user_b)

    elif user_a == '바위':

        if user_b == '가위':
            print('user1 승리')
            win_a += 1

        elif user_b == '바위':
            print('무승부')

        elif user_b == '보':
            print('user2 승리')
            win_b += 1

        else:
            print('user2 값 오류 ->', user_b)

    elif user_a == '보':

        if user_b == '가위':
            print('user2 승리')
            win_b += 1

        elif user_b == '바위':
            print('user1 승리')
            win_a += 1

        elif user_b == '보':
            print('무승부')

        else:
            print('user2 값 입력 오류 ->', user_b)

    else:
        print('user1 값 입력 오류 ->', user_a)

    print('user1', win_a, ':', 'user2', win_b)
    print('------------------------------------')

if win_a == 3:
    print('### user1 3선승! 최종 승리!! ###')
else:
    print('### user2 3선승! 최종 승리! ###')