from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
import re

# Chrome WebDriver 설정
chrome_driver_path = "C:/Users/dnltj/OneDrive/바탕 화면/GitHub_sub/OCR_Project/food_classification_modeling/fat_secret_data_crawling/etc/chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.get('https://www.ewangmart.com/goods/category.do?cate=15')
wait = WebDriverWait(driver, 10)
time.sleep(3)

# "더보기" 버튼 반복 클릭하여 모든 상품 로드
scroll_increment = 700

while True:
    try:
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(1)
        more_button = wait.until(EC.presence_of_element_located((By.ID, 'pageBtn')))
        more_button.click()
        time.sleep(2)
    except:
        break

# 최상단으로 스크롤 이동
driver.execute_script("window.scrollTo(0, 0);")
time.sleep(2)

# 모든 상품의 URL에서 gno 값 추출
pattern = r"gno=(\d+)"
products = []

product_elements = driver.find_elements(By.CSS_SELECTOR, '.thumb.type4 a') 
for element in product_elements:
    url = element.get_attribute('href')
    gno = re.search(pattern, url).group(1) if re.search(pattern, url) else None
    if gno:
        products.append(gno)

# JSON으로 저장
with open("product_data.json", "w", encoding="utf-8") as json_file:
    json.dump(products, json_file, ensure_ascii=False, indent=4)

driver.quit()