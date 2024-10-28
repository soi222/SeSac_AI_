"""
위의 코드는 더보기를 누른 뒤 다시 상품을 가져오지 못함
"""
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from googletrans import Translator  # Googletrans 라이브러리 임포트

# 저장할 파일 경로 설정
chrome_driver_path = "C:/Users/dnltj/OneDrive/바탕 화면/GitHub_sub/OCR_Project/food_classification_modeling/fat_secret_data_crawling/etc/chromedriver.exe"

# Service 객체 생성 및 드라이버 실행
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# 사이트 접속
url = 'https://www.ewangmart.com/goods/category.do?cate=15'
driver.get(url)

# 저장할 dir
save_directory = 'C:/Users/dnltj/OneDrive/바탕 화면/test_crawling/Bigmart_snacks'

# Googletrans 번역기 초기화
translator = Translator()

try:
    wait = WebDriverWait(driver, 10)
    
    # 상품 목록을 가져오기
    product_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.thumb.type4 a')))
    
    # 클릭한 상품 개수
    clicked_product_count = 0

    # 모든 상품에 대해 반복
    while clicked_product_count < 20:  # 20개 클릭 시 종료
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
            
            # 영어로 변환하고 띄어쓰기를 언더바(_)로 변경
            translated_title = translator.translate(title_text, dest='en').text
            safe_title = translated_title.replace(' ', '_')  # 공백을 언더바로 변경
            
            # 저장할 이미지 요소 찾기
            image_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#detail-section1 img')))
            for j, image_element in enumerate(image_elements[1:], start=2):  # 두 번째 이미지부터 시작
                # 이미지 URL 가져오기
                image_url = image_element.get_attribute('src')
                
                # 절대 URL 만들기
                if image_url.startswith('/'):
                    image_url = 'https://www.ewangmart.com' + image_url
                
                # 파일 이름 설정 (예: snack_image_2.jpg, snack_image_3.jpg 등)
                file_name = f"{safe_title}_image_{j}.jpg"
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
            
            clicked_product_count += 1  # 클릭한 상품 개수 증가
            
            # 상품 페이지 나가기 (이전 페이지로 돌아가기)
            driver.back()  # 이전 페이지로 돌아가기

            # 상품 목록을 다시 로드
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.thumb.type4 a')))
            product_links = driver.find_elements(By.CSS_SELECTOR, '.thumb.type4 a')  # 상품 목록 새로고침
            time.sleep(10)

            # 클릭한 상품이 20개 이상인지 확인
            if clicked_product_count >= 20:
                break

        # 더보기 버튼 클릭
        try:
            more_button = wait.until(EC.presence_of_element_located((By.ID, 'pageBtn')))
            more_button.click()
            time.sleep(2)  # 더보기 버튼 클릭 후 잠시 대기
            
            # 현재 페이지가 19 미만인지 확인
            current_page = int(driver.find_element(By.CSS_SELECTOR, '.currentPage').text)  # 현재 페이지 번호 가져오기
            if current_page < 19:
                print("현재 페이지가 19 미만이므로 크롤링을 종료합니다.")
                break
            
            # 상품 목록을 새로 가져오기
            product_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.thumb.type4 a')))
        except Exception as e:
            print(f"더보기 버튼 클릭 중 오류 발생: {e}")
            break

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    driver.quit()  # 드라이버 종료
