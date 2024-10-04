#선생님의 답
game_status = {'x_positions' : [], 'o_positions' : []} 

def empty_board(x_size = 3, y_size = 3, x_cell_size = 5, y_cell_size = 3):
    """Create an empty board. 

    The board is made of horizontal lines, made with - and vertical lines, made with |. 

    (optional) When there are no x_cell_size and y_cell_size arguments, default to arbitary size of your choice. Just make it consistent. 

     ---------- ---------- ----------
    |          |          |          |
    |    X     |    O     |    X     |
    |          |          |          |
     ---------- ---------- ----------
    |          |          |          |
    |          |    O     |    X     |
    |          |          |          |
     ---------- ---------- ----------
    |          |          |          |
    |    O     |    X     |    O     |
    |          |          |          |
     ---------- ---------- ----------
    """
    hline =  (' ' + '-' * x_cell_size ) * x_size #윗라인 출력

    for y in range(y_size):
        print(hline) #중요 : 반복이 되는 부분을 생각하기, 1. 동일한 사이즈가 반복되는 경우 2. 프랙탈과 같이 일정한 크기로 줄어드는 경우
        for z in range(y_cell_size): #임의적으로 셀의 크기를 정해둔것, 수정될 경우를 대비해서 cellsize설정
            for x in range(x_size): #세로 라인 출력
                print('|' + ' ' * x_cell_size, end = '')
            print('|')
    print(hline)    
    
def play(game_status, x_or_o, coordinate):
    """Main function for simulating tictactoe game moves. 

    Tictactoe game is executed by two player's moves. In each move, each player chooses the coordinate to place their mark. It is impossible to place the mark on already taken position. 

    A move in the tictactoe game is composed of two components; whether who ('X' or 'O') made the move, and how the move is made - the coordinate of the move. 

    Coordinate in our tictactoe system will use the coordinate system illustrated in the example below. 
    
    Example 1. 3 * 4 tictactoe board. 
    
         ---------- ---------- ----------
        |          |          |          |
        |  (0,0)   |  (1,0)   |  (2,0)   |
        |          |          |          |
         ---------- ---------- ----------
        |          |          |          |
        |  (0,1)   |  (1,1)   |  (2,1)   |
        |          |          |          |
         ---------- ---------- ----------
        |          |          |          |
        |  (0,2)   |  (1,2)   |  (2,2)   |
        |          |          |          |
         ---------- ---------- ----------
        |          |          |          |
        |  (0,3)   |  (1,3)   |  (2,3)   |
        |          |          |          |
         ---------- ---------- ----------
        """
    #안되는 경우: 놓은 자리에 놓으면 안된다
    if coordinate in game_status['x_positions'] + game_status['o_positions']: #game_status["x_positions"] : 이때까지 x가 놓인 위치들
        assert False

    if x_or_o == 'X': #x가 입력한 경우
        game_status['x_positions'].append(coordinate) 
    elif x_or_o == 'O': #o가 입력한 경우
        game_status['o_positions'].append(coordinate) #여기서 elif를 사용하는 이유는 대소문자도 다르게 구분하기때문에, 작은 오류를 막기위함
    else: #else는 쓰지 않아도 패스되기때문에 괜찮음
        raise ValueError(f'x_or_o should be one of X or O; got {x_or_o}')

def check_winlose(game_status):
    """Check the game status; game status should be one of 'X wins', 'O wins', 'tie', 'not decided'. 
    """
    winning_positions = [
        [(0,0), (1,0), (2,0)],  
        [(0,1), (1,1), (2,1)], 
        [(0,2), (1,2), (2,2)], 
        [(0,0), (0,1), (0,2)], 
        [(1,0), (1,1), (1,2)], 
        [(2,0), (2,1), (2,2)], 
        [(0,0), (1,1), (2,2)], 
        [(2,0), (1,1), (0,2)],
    ]

    if determine_if_x_wins(game_status, winning_positions):
        return 'X wins'
    elif determine_if_o_wins(game_status, winning_positions):
        return 'O wins'
    elif len(game_status['x_positions'] + game_status['o_positions']) == 9:
        return 'tie' 
    else:
        return 'not decided' 

def determine_if_x_wins(game_status, winning_positions):
    x_pos = game_status['x_positions']
    for win in winning_positions:
        a, b, c = win 
        if a in x_pos and b in x_pos and c in x_pos:
            return True
    return False 

def determine_if_o_wins(game_status, winning_positions):
    o_pos = game_status['o_positions']
    for win in winning_positions:
        a, b, c = win 
        if a in o_pos and b in o_pos and c in o_pos:
            return True
    return False 

def display(game_status, x_size = 3, y_size = 3, x_cell_size = 5, y_cell_size = 3):
    """Display the current snapshot of the board. 

    'Snapshot' should contain following components. 

    - The board itself 
    - Moves that are already made

    For clarification, see provided examples. 

    Example 1. 
    When TictactoeGame instance t have following attributes; 
    - x_positions = [(0,0), (2,0), (2,1), (1,2)]
    - o_positions = [(1,0), (1,1), (0,2), (2,2)]

    t.display()
    >> 
     ---------- ---------- ----------
    |          |          |          |
    |    X     |    O     |    X     |
    |          |          |          |
     ---------- ---------- ----------
    |          |          |          |
    |          |    O     |    X     |
    |          |          |          |
     ---------- ---------- ----------
    |          |          |          |
    |    O     |    X     |    O     |
    |          |          |          |
     ---------- ---------- ----------

    """
    hline =  (' ' + '-' * x_cell_size ) * x_size

    for y in range(y_size):
        print(hline)
        for z in range(y_cell_size):
            for x in range(x_size):
                if z == 1:
                    if (x, y) in game_status['x_positions']:
                        print('|' + ' ' * (x_cell_size-1) + 'X', end = '')
                    elif (x, y) in game_status['o_positions']:
                        print('|' + ' ' * (x_cell_size-1) + 'O', end = '')
                    else:
                        print('|' + ' ' * x_cell_size, end = '')
                else:
                    print('|' + ' ' * x_cell_size, end = '')
            print('|')
    print(hline)    


if __name__ == '__main__':
    # empty_board(x_size = 3, y_size = 3, x_cell_size = 5, y_cell_size = 3)
    game_status = {'x_positions' : [(0,0)], 'o_positions' : [(1,0)]} 

    display(game_status)
game_status = {'x_positions' : [], 'o_positions' : []} #x와 o의 위치를 파악하고 넣어두는 데 사용

def empty_board(x,y):
    """Create an empty board. 

    The board is made of horizontal lines, made with - and vertical lines, made with |. 

    (optional) When there are no x_cell_size and y_cell_size arguments, default to arbitary size of your choice. Just make it consistent. 
    """
    for i in range(x): 
        print(' '+('  -------')*y)
        
        for j in range(3):
            print('|' + ('         |' * y))

    print((' '+('  -------')*y))


def play(game_status, x_or_o, coordinate):
    """Main function for simulating tictactoe game moves. 

    Tictactoe game is executed by two player's moves. In each move, each player chooses the coordinate to place their mark. It is impossible to place the mark on already taken position. 

    A move in the tictactoe game is composed of two components; whether who ('X' or 'O') made the move, and how the move is made - the coordinate of the move. 

    Coordinate in our tictactoe system will use the coordinate system illustrated in the example below. 
    
    Example 1. 3 * 4 tictactoe board. 
    
         ---------- ---------- ----------
        |          |          |          |
        |  (0,0)   |  (1,0)   |  (2,0)   |
        |          |          |          |
         ---------- ---------- ----------
        |          |          |          |
        |  (0,1)   |  (1,1)   |  (2,1)   |
        |          |          |          |
         ---------- ---------- ----------
        |          |          |          |
        |  (0,2)   |  (1,2)   |  (2,2)   |
        |          |          |          |
         ---------- ---------- ----------
        |          |          |          |
        |  (0,3)   |  (1,3)   |  (2,3)   |
        |          |          |          |
         ---------- ---------- ----------
        """
    #안되는 경우 : 놓은 자리에 놓으면 안된다
    if coordinate == game_status['x_positions'] + game_status['o_positions']:
        print("x_position과 o_position에 중복되는 값을 둘 수 없습니다.")

    elif x_or_o in 'X': #X가 입력한 경우
        a = game_status['x_positions'].append(coordinate)
        print(f"x_player가 {a}로 움직였습니다.")
    else: #O가 입력한 경우
        b = game_status['o_positions'].append(coordinate)
        print(f"o_player가 {b}로 움직였습니다.") 

winning_positions = [
        [(0,0),(0,1),(0,2)],
        [(0,0),(1,1),(2,2)],
        [(0,0),(1,0),(2,0)],
        [(1,0),(1,1),(1,2)],
        [(2,0),(1,1),(0,2)],
        [(2,0),(2,1),(2,2)],
        [(0,1),(1,1),(2,1)],
        [(0,2),(1,2),(2,2)]
    ]

def check_winlose(game_status):
    """Check the game status; game status should be one of 'X wins', 'O wins', 'tie', 'not decided'. 
    """

    if game_status['o_positions'] in winning_positions:
        print("O wins")
    elif game_status['x_positions'] in winning_positions:
        print("X wins")
    elif game_status['x_positions'] + game_status["o_positions"]  == 9:
        print("tie")
    else:
        print("not decided")

def display(game_status):
    """Display the current snapshot of the board. 

    'Snapshot' should contain following components. 

    - The board itself 
    - Moves that are already made

    For clarification, see provided examples. 

    Example 1. 
    When TictactoeGame instance t have following attributes; 
    - x_positions = [(0,0), (2,0), (2,1), (1,2)]
    - o_positions = [(1,0), (1,1), (0,2), (2,2)]

    t.display()
    >> 
     ---------- ---------- ----------
    |          |          |          |
    |    X     |    O     |    X     |
    |          |          |          |
     ---------- ---------- ----------
    |          |          |          |
    |          |    O     |    X     |
    |          |          |          |
     ---------- ---------- ----------
    |          |          |          |
    |    O     |    X     |    O     |
    |          |          |          |
     ---------- ---------- ----------

    """
def display(game_status):#(row칸 수 ,column칸 수)
      print(' '+('  -------')*3)
      for i in range(3):
            print(' '+('  -------')*3)
            for j in range(3):
                print('|' + ('         |' * 3))
                for z in range(3):
                  if game_status == (range(4),range(4)):
                    print('|' + ('   X   |' * 3))
                  elif game_status == (range(4),range(4)):
                    print('|' + ('   O   |' * 3))
            print((' '+('  -------')*y))

display(0,0)
