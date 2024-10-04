from util import company_lists, plot_line_graph
from random import random
import os 
from collections import defaultdict

class Stock:
    #stock_history : 이전까지의 주식현황
    HISTORY_DIR = 'stock_history'
    def __init__(self, name):
        self.name = name #주식이름
        self.initial_price = 10000
        self.price_history = [10000]
        self.momentum = 0
        self.momentum_upper_bound = max(abs(random()-0.5), 0.5)
        self.momentum_lower_bound = -max(abs(random()-0.5), 0.5)
        self.price = self.initial_price

    def __hash__(self):
        return hash(self.name)
    
    def step(self, market): #랜덤한 주가변경
        if random() < 0.05:
            self.price = self.price * 1.10
        elif random() > 0.95:
            self.price = self.price * 0.80
        else:
            self.momentum += (random() - 0.5) * 0.1 #+ self.momentum
            if self.momentum_upper_bound < self.momentum:
                self.momentum = self.momentum_lower_bound
            elif self.momentum_lower_bound > self.momentum:
                self.momentum = self.momentum_lower_bound
            delta = random() - 0.5 + self.momentum + market.momentum 
            self.price += self.momentum * self.price 
        self.price_history.append(self.price)

    def plot_history(self):
        if not os.path.exists(Stock.HISTORY_DIR):
            os.makedirs(Stock.HISTORY_DIR)
        
        plot_line_graph(self.price_history, save_to = f'stock_history/{self.name}.png', title = f'Price graph of {self.name}', x_label = 'time', y_label = '{self.name} price')
         

class StockMarket:
    def __init__(self, listed_stocks):
        self.listed_stocks = listed_stocks
        self.momentum = 0.01

    def step(self):
        for stock in self.listed_stocks:
            stock.step(self)

class Investor:
    def __init__(self, name = 'sh', initial_asset = 10000000, strategy = lambda investor, market:None):
        self.name = name 
        self.asset = initial_asset
        self.cash = initial_asset #가지고 있는 현금
        self.asset_history = [initial_asset]
        self.portfolio = defaultdict(float)
        self.strategy = strategy

    def buy(self, stock, amount): #amount 소숫점도 가능하다고 생각
        #cash + stock_value : 주식가치
        if self.cash - stock.price * amount >= 0: 
            self.portfolio[stock] += amount
            self.cash -= stock.price * amount
        else:
            print('Out of money')

    def sell(self, stock, amount):
        if stock in self.portfolio and self.portfolio[stock] >= amount:
            self.portfolio[stock] -= amount 
            self.cash += stock.price * amount 
        else:
            print('Not enough stocks')

    def buy_or_sell(self, market):
        #inverstor함수 이용
        self.strategy(self, market)
        stock_asset = 0
        for stock, amount in self.portfolio.items():
            stock_asset += stock.price * amount
        self.asset = stock_asset + self.cash 
        self.asset_history.append(self.asset)

    def plot_history(self):
        plot_line_graph(self.asset_history, save_to = f'{self.name}.png', title = f'Asset History of {self.name}', x_label = 'time', y_label = '{self.name} Asset')

def simulate(strategy = lambda investor, market:None, n_steps = 100, n_company = 10):
    #앞으로 어떤식으로 플레이할것인지에 대한 전략 설정
    #steps : 몇번의 변화를 확인할건지
    investor = Investor(strategy = strategy)
    stocks = [] #ncompany개만큼 만든 랜덤한 수
    
    company_list = []

    if not os.path.exists(Stock.HISTORY_DIR):
        company_list = company_lists(n_company)
    else:
        company_list = [e.strip('.png') for e in os.listdir(Stock.HISTORY_DIR)]
        
        if len(company_list) > n_company:
            company_list = company_list[:n_company]
        else:
            company_list = company_list + company_lists(n_company - len(company_list))

    for name in company_list:
        stocks.append(Stock(name))

    market = StockMarket(stocks)

    for step in range(n_steps):
        market.step() #= stockmarket(market)
        #시장이 변화하는 것을 확인
        investor.buy_or_sell(market)

    for stock in stocks:
        stock.plot_history()
    investor.plot_history()

def my_strategy(investor, market):
    if Stock.initial_price == max(Stock.initial_price):
        Investor.buy()
    elif Stock.initial_price == min(Stock.initial_price):
        Investor.sell()
    
    # market.listed_stocks
    print(f"{investor.name} on market.")

    


if __name__ == '__main__':
    simulate(strategy = my_strategy)

