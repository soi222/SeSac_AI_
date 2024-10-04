import aiohttp
import asyncio
from bs4 import BeautifulSoup

# 언론사 리스트업
async def crawl_press_names_and_codes():
    """Make the dict that has press code as key, and press name as value. Crawl from https://media.naver.com/channel/settings."""
    url = 'https://media.naver.com/channel/settings'
    code2name = {}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                for li in soup.find_all('li', {'class': 'ca_item _channel_item'}):
                    press_name = li.find('div', {'class': 'ca_name'}).text
                    press_code = li['data-office']
                    code2name[press_code] = press_name 
    return code2name

# 기자 리스트업
async def crawl_journalist_info_pages(code2name):
    """Accepts press code - press name dict, and return dict having press code as key, and 2-tuple of (press name, list of 2-tuple containing journalist name and their link) as value."""
    res = {}
    
    async with aiohttp.ClientSession() as session:
        for press_code, press_name in code2name.items():
            url = f'https://media.naver.com/journalists/whole?officeId={press_code}'
            async with session.get(url) as response:
                journalist_list = []
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    for li in soup.find_all('li', {'class': 'journalist_list_content_item'}):
                        info = li.find('div', {'class': 'journalist_list_content_title'})
                        a = info.find('a')
                        journalist_name = a.text.strip('기자')
                        journalist_link = a['href']
                        journalist_list.append((journalist_name, journalist_link))
                res[press_code] = (press_name, journalist_list)
    return res

# 메인 실행부
async def main():
    code2name = await crawl_press_names_and_codes()
    code2info = await crawl_journalist_info_pages(code2name)
    # 여기서 code2info를 처리하는 로직 추가 가능

if __name__ == '__main__':
    asyncio.run(main())