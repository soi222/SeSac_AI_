import asyncio
from time import time, sleep
from playwright.async_api import async_playwright

async def login_connection(page):
    login_button = await page.wait_for_selector("a[onclick='return m_login_link()']")
    await login_button.click()

async def ktx_ticketing_id(page, search_keyword = "1971869731",timeout = 5000):
    id = await page.wait_for_selector("#txtMember")
    await id.type(search_keyword)

async def ktx_ticketing_pwd(page, search_keyword = "rpwkfl0719@"):
    pwd = await page.wait_for_selector("#txtPwd")
    await pwd.type(search_keyword)

async def ktx_login(page):
    execute_login = await page.wait_for_selector(".btn_login")
    await execute_login.click()
    await page.wait_for_selector("#contents")

# async def depart_choice(page):
#     elem = await page.query_selector_all(".btn_sch_r")
#     execute_depart = elem[0]
#     await execute_depart.click()
#     await page.wait_for_selector("")

async def date_choice(page, day_id = "d20240914"):
    elem = await page.query_selector_all(".btn_sch_r")
    if len(elem) > 2:
            execute_date = elem[2]
            await execute_date.click()

    calendar = await page.wait_for_selector(".td.dayBlue")  # 날짜 선택 캘린더의 셀렉터
    await calendar.click()

    date_selector = f"xpath=//td[contains(text(), '{day_id[-2:]}')]" 
    date_element = await page.wait_for_selector(date_selector)
    await date_element.click()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless = False)
        context = await browser.new_context()
        page = await browser.new_page()
        await page.goto("https://www.letskorail.com/ebizprd/prdMain.do")
        
        await login_connection(page)
        await ktx_ticketing_pwd(page, search_keyword="rpwkfl0719@")
        await ktx_login(page)
        await date_choice(page, day_id = "d20240914")
        

        sleep(30)
asyncio.run(main())
