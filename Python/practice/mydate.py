class MyDate:

    def __init__(self, year = 0, month = 0, day = 0, hour = 0, minute = 0, sec = 0): 
        #year
        def valid_year(year):
            if 0 <= year <= 2100:
                return True
            return False
                    
        assert valid_year(year),"Year Error"
        self.year = year

        #month
        def valid_month(month):
            if 0 <= month < 13:
                return True
            return False
            
        
        assert valid_month(month), "Month Error"
        self.month = month

        #day
        last_31 = [1,3,5,7,8,10,12]
        last_30 = [4,6,9,11]

        def valid_day(year,month, day):
            yoon = year % 4 == 0 and year % 400 == 0

            if month == 2:
                if yoon or (year % 100 != 0):
                   return 0 <= day <= 28
            
                else:
                    return 0 <= day <= 29
            
            elif month in last_30:
                return 0 <= day <= 30
            
            elif month in last_31:
                return 0 <= day <= 31
            
            elif month == 0:
                return True

            return False 

        assert valid_day(year, month, day), "Day Error"
        self.day = day

        #hour
        def valid_hour(hour):
            if 0 <= hour <= 23:
                return True
            return False
            
        assert valid_hour(hour), "Hour Error"
        self.hour = hour    

        #minute
        def valid_minute(minute):
            if 0 <= minute <= 59:
                return True
            return False
            
        assert valid_minute(minute), "Minute Error"
        self.minute = minute

        #sec
        def valid_sec(sec):
            if 0 <= sec <= 59:
                return True
            return False

        assert valid_sec(sec), "Sec Error"
        self.sec = sec

        #total
        # print(f"{year}년{month}월{day}일, {hour}:{minute}:{sec}")


    def __add__(self, other): #mydate끼리 더하는 함수
        self.other = other

        sec_a = (self.sec + other.sec) % 60 
        sec_add = (self.sec + other.sec) // 60
    
        minute_a = (self.minute + other.minute + sec_add) % 60 #괄호 안에 sec_a 더하기
        minute_add = (self.minute + other.minute + sec_add) // 60

        hour_a = (self.hour + other.hour + minute_add) % 24 
        hour_add = (self.hour + other.hour + minute_add) // 24

        day_a = (self.day + other.day + hour_add) 

        month_a = (self.month + other.month)

        year_a = (self.year + other.year)

        #day
        while True:
            if month_a > 12:
                month_a -= 12
                year_a += 1

            if month_a == 2:
                if (year_a % 4 == 0 and year_a % 100 != 0) or (year_a % 400 == 0):
                    last_day = 29 
                else: 
                    last_day = 28

            elif month_a in [4, 6, 9, 11]:
                last_day = 30

            else:
                last_day = 31
            
            if day_a <= last_day:
                break
            day_a -= last_day
            month_a += 1

        return MyDate(year = year_a, month= month_a, day= day_a, hour= hour_a, minute=minute_a, sec=sec_a)
        

    def __sub__(self, other): # date끼리 빼는 함수
        
        #year
        year_sub = self.year - other.year

        # sec
        sec_sub = (self.sec - other.sec) % 60  # 나머지
        sec_sub_a = (self.sec - other.sec) // 60  # 몫

        # minute
        minute_sub = (self.minute - other.minute - sec_sub_a) % 60
        minute_sub_a = (self.minute - other.minute) // 60

        # hour
        hour_sub = (self.hour - other.hour) % 24
        hour_sub_a = (self.hour - other.hour - minute_sub_a) // 24
        

        # month
        month_sub = self.month - other.month

        #day
        day_sub = self.day - other.day
        
        if month_sub == 2:
            yoon = (year_sub % 4 == 0 and year_sub % 100 != 0) or (year_sub % 400 == 0)
            day_sub += 29 if yoon else 28
            month_sub -= 1

        elif month_sub in [4, 6, 9, 11]:
            day_sub += 31
            month_sub -= 1

        elif month_sub in [1,3,5,7,8,10,12]:
            day_sub += 30
            month_sub -= 1

        if month_sub < 0:
            month_sub += 12
            year_sub -= 1

        return MyDate(year=year_sub, month=month_sub, day=day_sub, hour=hour_sub, minute=minute_sub, sec=sec_sub)

    def __eq__(self, other): #d1,d2끼리 같은지 확인, 다른 지 확인은 not __eq
        print(self, other)
        return (self.year == other.year and \
            self.month == other.month and \
            self.day == other.day and \
            self.hour == other.hour and \
            self.minute == other.minute and \
            self.sec == other.sec)
        
    def __lt__(self, other): #d1 < d2 인 경우 
        if self.year < other.year:
            return True
        elif self.year == other.year:
            if self.month < other.month:
                return True
            elif self.month == other.month:
                if self.day < other.day:
                    return True
                elif self.day == other.day:
                    if self.hour < other.hour:
                        return True
                    elif self.hour == other.hour:
                        if self.minute < other.minute:
                            return True
                        elif self.minute == other.minute:
                            if self.sec < other.sec:
                                return True
    
    def __le__(self, other):# d1 <= d2인 경우
        if self.year < other.year:
            return True
        elif self.year == other.year:
            if self.month < other.month:
                return True
            elif self.month == other.month:
                if self.day < other.day:
                    return True
                elif self.day == other.day:
                    if self.hour < other.hour:
                        return True
                    elif self.hour == other.hour:
                        if self.minute < other.minute:
                            return True
                        elif self.minute == other.minute:
                            if self.sec <= other.sec:
                                return True
        return False


    def __gt__(self, other):#d1 > d2 인 경우
        if self.year > other.year:
            return True
        elif self.year == other.year:
            if self.month > other.month:
                return True
            elif self.month == other.month:
                if self.day > other.day:
                    return True
                elif self.day == other.day:
                    if self.hour > other.hour:
                        return True
                    elif self.hour == other.hour:
                        if self.minute > other.minute:
                            return True
                        elif self.minute == other.minute:
                            if self.sec > other.sec:
                                return True
        return False
    
    def __ge__(self, other): # d1 >= d2
        if self.year > other.year:
            return True
        elif self.year == other.year:
            if self.month > other.month:
                return True
            elif self.month == other.month:
                if self.day > other.day:
                    return True
                elif self.day == other.day:
                    if self.hour > other.hour:
                        return True
                    elif self.hour == other.hour:
                        if self.minute > other.minute:
                            return True
                        elif self.minute == other.minute:
                            if self.sec >= other.sec:
                                return True
        return False

         
    def __str__(self):
        return f"{self.year}년 {self.month}월 {self.day}일, {self.hour}:{self.minute}:{self.sec}"


if __name__ == '__main__':
    #   d0 = MyDate()
    d1 = MyDate(2022, 4, 1, 14, 30)
    d2 = MyDate(2024, 8, 23, 23, 10) # should raise an error 
    # d3 = MyDate(2024, 2, 30)

    d3 = MyDate(day = 1) 
    #print(d1 - d3)
    assert d1 + d3 == MyDate(2022, 4, 2, 14, 30)
    assert d1 - d3 == MyDate(2022, 3, 31, 14, 30) 
   
    print( d1 < d2 )#과거보다 현재가 더 큼

    d4 = MyDate(2022, 1, 31)
    d5 = MyDate(day = 30)

    print(d4 + d5)
    assert d4 + d5 == MyDate(2022, 3, 2)
    print(True)

