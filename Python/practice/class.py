class Dog:
    breed = "chichu"
    color = "white and brown"
    type = "cute"
    weight = 6

    def action(run):
        print(f"Dog is {run}")


class Youtuber:
    link = "http://www.youtube.com@suka"
    number_of_subscribers = 939000
    number_of_videos = 584
    number_of_views = 392918254
    date_of_creation = "20210916"
    country = "대한민국"
    
    def hello(x):
        print(x)
        print("hello World")

    def __init__(self,link):
        self.link = link

suka = Youtuber()
print(suka.link)

#주의
y = Youtuber()
y.hello() # = Youtuber.hello(y)

# 위의 경우 def hello에 인풋값이 없는데 y라는 인풋이 들어왔기 때문에 에러발생
#    def hello(x):
#        print(x)
#        print("hello World")
#위와 같이 수정하지 않으면 오류 발생

#출력
슈카 = Youtuber()
print(슈카.link)
print()
슈카.link = "www.naver.com"
print(슈카.link)

#class 수정
침착맨 = Youtuber(link = "http://www.youtube.com@chimchakman",)
# = Youtuber.__init__(침착맨, link = "http://www.youtube.com@chimchakman")
