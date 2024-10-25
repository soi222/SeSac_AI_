import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 저장할 파일 경로 설정
chrome_driver_path = "C:/Users/user/Desktop/project/testset_crawling/chromedriver-win64/chromedriver.exe"

# Service 객체 생성 및 드라이버 실행
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# 사이트 접속
url = 'https://www.ewangmart.com/goods/category.do?cate=15'
driver.get(url)

# 저장할 dir
save_directory = 'C:/Users/user/Desktop/project/testset_crawling/Bigmart_snacks'

try:
    wait = WebDriverWait(driver, 10)
    
    # 상품 목록을 가져오기
    product_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.thumb.type4 a')))
    
    # 모든 상품에 대해 반복
    for i in range(len(product_links)):
        # 요소 스크롤하여 보이게 하기
        driver.execute_script("arguments[0].scrollIntoView();", product_links[i])
        
        # 잠시 대기
        time.sleep(1)  # 필요한 만큼 대기 조정
        
        # 각 상품 클릭 (JavaScript 클릭 사용)
        driver.execute_script("arguments[0].click();", product_links[i])
        
        # 상품 페이지에서 제목 가져오기
        title_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.title.type2 span')))
        title_text = title_element.text.strip()  # 텍스트 가져오기 및 공백 제거
        
        # 파일명에 사용할 수 있도록 정리
        safe_title = title_text.replace('/', '_').replace('\\', '_')  # 파일명에 사용할 수 없는 문자 제거

        # 모든 이미지 요소 찾기
        image_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#detail-section1 img')))
        
        for j, image_element in enumerate(image_elements[1:], start=2):  # 두 번째 이미지부터 시작
            # 이미지 URL 가져오기
            image_url = image_element.get_attribute('src')
            
            # 절대 URL 만들기
            if image_url.startswith('/'):
                image_url = 'https://www.ewangmart.com' + image_url
            
            # 파일 이름 설정 (예: Bigmart_snacks_2.jpg, Bigmart_snacks_3.jpg 등)
            file_name = f"{safe_title}_{j}.jpg"
            file_path = os.path.join(save_directory, file_name)

            # 이미지 다운로드
            response = requests.get(image_url)
            
            # 이미지 저장
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"이미지 저장 완료: {file_path}")
            else:
                print("이미지를 다운로드할 수 없습니다.")
        
        # 상품 페이지 나가기 (이전 페이지로 돌아가기)
        driver.back()  # 이전 페이지로 돌아가기

        # 상품 목록을 다시 로드
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.thumb.type4 a')))
        product_links = driver.find_elements(By.CSS_SELECTOR, '.thumb.type4 a')  # 상품 목록 새로고침
        time.sleep(10)

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    driver.quit()  # 드라이버 종료
