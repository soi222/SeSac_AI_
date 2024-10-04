class MyDate:
    def __init__(self, year, month, day, hour, minute, sec):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.sec = sec

    def __lt__(self, other):
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
        return False

# Create two date objects
d1 = MyDate(2024, 8, 8, 14, 30, 0)
d2 = MyDate(2024, 8, 8, 15, 0, 0)

# Perform the comparison and print the result
print("Is d1 < d2?", d1 < d2)  
# # This should print: Is d1 < d2? True