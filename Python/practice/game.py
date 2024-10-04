import random

class Game:
    def __init__(self, players):
        self.players = players 

        if players == {}:
            print("players list empty")
        
    def play_match(self, player1, player2):
        # player1, player2의 win_lose_history를 update하고 
        # elo rating 알고리즘에 따라 각자의 current_rating을 update할 것 
        # https://namu.wiki/w/Elo%20%EB%A0%88%EC%9D%B4%ED%8C%85 참고 
        #pa = pb + K * (W - We)
        #pa = 경기 후의 점수
        #pb 경기 전 점수
        # K 가중치
        # W 경기결과(승리 시 1, 무승부 0.5, 패배 시 0)
        # We 예측된 승률

        Pop = current_rating
        Pme = 
        
        We = 1 / (10**((Pop - Pme)//400) + 1)
        


    def match_players(self):
        pass
        # player들을 current_rating을 기반으로 
        
    def simulate(self):
        pass 
    
class Player:
    def __init__(self, player_id, initial_rating = 1000, actual_rating = 1000): #initial = 게임 기본점수, #actal = 실력 점수
        self.win_lose_history = []
        self.current_rating = initial_rating
        self.actual_rating = actual_rating
        pass

    def __str__(self):
        return str(self.player_id)


if __name__ == '__main__':
    pass
    # players = {}

    # for i in range(1,1001):
    #     player_id = f'player_{i}'
    #     players[player_id] = player_id, actual_rating = random.gauss(1000, 100)
    


