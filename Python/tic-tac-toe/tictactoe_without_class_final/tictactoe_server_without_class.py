from tictactoe_without_class import check_winlose, play, display 

def play_game(x_player, o_player):
    game_status = {'x_positions' : [], 'o_positions' : []} 
    x_or_o = 'X'
    
    while check_winlose(game_status) == 'not decided': #기존 파일과 오류명이 같아야함
        print('==============')
        x_positions = game_status['x_positions']
        o_positions = game_status['o_positions']
        
        if x_or_o == 'X':
            x_move = x_player(x_or_o, x_positions, o_positions)
            play(game_status, x_or_o, x_move)
            x_or_o = 'O'
            print(f'x_player moved to {x_move}')
        else:
            o_move = o_player(x_or_o, x_positions, o_positions)
            play(game_status, x_or_o, o_move)
            x_or_o = 'X'
            print(f'o_player moved to {o_move}')
        display(game_status)
    print(check_winlose(game_status))
    return game_status 

from random import choices
def smart_player(x_or_o, x_positions, o_positions): #random이지만 똑똑하게 둘 수 있도록 만들자

        
# (1,1)를 차지한 경우
# 1. random_player가 둔 곳을 제외한 나머지 셀 중 하나 두기[(0,0),(1,0),(2,0),(0,1),(0,2),(1,2),(2,2)]
# 2. random_player가 둔 곳을 제외하고 나머지 중 winning_positions에 해당되는 빈 셀이 있는지 확인
# 3. 빈 곳이 있다면 빈 셀채우기, 아니라면 나머지 셀에 두기

# (1,1)을 차지하지 못한 경우
# 1. [(0,0),(1,0),(2,0),(0,1),(0,2),(1,2),(2,2)]중 하나 두기
# 2. random_player가 둔 곳에 winning_positions에 해당되는 빈 셀이 있는지 확인
# 3. 해당 셀을 채우기, 없다면 
# 4. 
    winning_positions = [
    [(0,0), (1,0), (2,0)] or [(0,1), (1,1), (2,1)] or [(0,2), (1,2), (2,2)] or [(0,0), (0,1), (0,2)] or [(1,0), (1,1), (1,2)] or[(2,0), (2,1), (2,2)] or[(0,0), (1,1), (2,2)] or [(2,0), (1,1), (0,2)],
    ]

    a = [(0,1),(0,2)] or [(1,1),(2,2)] or [(1,0),(2,0)] #(0,0)
    b = [(0,0),(0,2)] or [(1,1),(2,1)] #(0,1)
    c = [(0,0),(0,1)] or [(2,0),(1,1)] or [(1,2),(2,2)] #(0,2)
    d = [(0,0),(2,0)] or [(1,2),(1,1)]  #(1,0)
    e = [(1,0),(1,1)] or [(0,2),(2,2)] #(1,2)
    f = [(0,0),(1,0)] or [(2,1),(2,2)] or [(1,1),(0,2)]#(2,0)
    g = [(2,0),(2,2)] or [(0,1),(1,1)]#(2,1)
    h = [(0,2),(1,2)] or [(2,0),(2,1)] or [(0,0),(1,1)] #(2,2)

    total = [(0, 0), (1, 0), (2, 0), (0, 1), (0, 2), (1, 2), (2, 2)]

    #가운데를 차지한 경우
    if x_or_o == "X":
        move = (1,1)
        x_positions.append(move)
        total.remove(o_positions)
        print('|' + ' ' * (display(x_cell_size-1)) + 'X', end = '')

        if x_positions == a:
            move(0,0)
            x_positions.append(move)
            print('|' + ' ' * (x_cell_size-1) + 'X', end = '')
        
        elif x_positions == b:
            move(0,1)
            x_positions.append(move)
            total.remove(o_positions)
            print('|' + ' ' * (display(x_cell_size-1)) + 'X', end = '')
        
        elif x_positions == c:
            move(0,2)
            x_positions.append(move)
            total.remove(o_positions)
            print('|' + ' ' * (display(x_cell_size-1)) + 'X', end = '')

        elif x_positions == d:
            move(1,0)
            x_positions.append(move)
            total.remove(o_positions)
            print('|' + ' ' * (display(x_cell_size-1)) + 'X', end = '')        

        elif x_positions == e:
            move(2,0)
            x_positions.append(move)
            total.remove(o_positions)
            print('|' + ' ' * (display(x_cell_size-1)) + 'X', end = '')

        elif x_positions == f:
            move(2,1)
            x_positions.append(move)
            total.remove(o_positions)
            print('|' + ' ' * (display(x_cell_size-1)) + 'X', end = '')

        elif x_positions == g:
            move(2,1)
            x_positions.append(move)
            total.remove(o_positions)
            print('|' + ' ' * (display(x_cell_size-1)) + 'X', end = '')

        elif x_positions == h:
            move(2,2)
            x_positions.append(move)
            total.remove(o_positions)
            print('|' + ' ' * (display(x_cell_size-1)) + 'X', end = '')
           
        

    #가운데를 차지하지 못한 경우
    elif random_player in x_positions:
        move = choices([(0,0),(1,0),(2,0),(0,1),(0,2),(1,2),(2,2)])
        if x_positions == winning:
            winning_positions.remove(move)

            
        
if __name__ == '__main__':
    from player import random_player #이렇게 두면 컴퓨터가 둘이 싸우는 것
    play_game(smart_player, random_player)


random_player : 아무곳에 두는 플레이어
smart_player: input, output을 정할 수 없음, 