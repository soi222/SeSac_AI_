import requests 
from bs4 import BeautifulSoup

def crawl_breaking_news_list():
    news_url = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&sid1=001&sid2=140&oid=001&isYeonhapFlash=Y&aid=0014907888'

    response = requests.get(news_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        td = soup.find("td",{"class":"content"})

        for li in td.find_all("li"):
            try:
                if li['data-comment'] is not None:
                    a = li.find("a")
                    link = a["href"]
                    text = a.text
                    print(link, text)

            except KeyError:
                pass

#각 언론사별 top랭킹 링크, 제목
def crawl_ranking_news():
    ranking_url = 'https://news.naver.com/main/ranking/popularDay.naver'

    response = requests.get(ranking_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        divs = soup.find_all("div",{"class":"rankingnews_box"})

        for div in divs:
            name = div.strong.text
            print("🌏 언론사 :",name)
            
            for li in div.find_all("li"):
                a = li.find("a")
                if a is not None:
                    link = a["href"]
                    text = a.text
                    print(text,link)
                    print()



#선생님ver
def crawl_ranking_news_teacher():
    ranking_url = 'https://news.naver.com/main/ranking/popularDay.naver'

    response = requests.get(ranking_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

    for div in soup.find_all("div", {"class":"rankingnews_box"}):
        press_name = div.find("strong")
        print("============")
        print(press_name.text)

        for li in div.find_all("li"):
            content = li.find("div",{"class":"list_content"})
            if content is not None:
                a = content.find("a")
                print(a["href"], a.text)

if __name__ == '__main__':
    #crawl_breaking_news_list()
    #crawl_ranking_news()s
    crawl_ranking_news_teacher()
