# 라이브러리 추가
import pymysql

# 연결자 생성
conn = pymysql.connect(host='localhost', user='root',
                       password='root', db='ShopDB', charset='utf8')

# 커서 생성
curs = conn.cursor()

# 전체 제품 목록 리스트
productList = []

'''
# 예시
productList = [
    {제품번호 : p0001, 제품명 : 노트북, 가격 : 1000000, 수량 : 3},
    {제품번호 : p0002, 제품명 : 마우스, 가격 : 10000, 수량 : 20},
]
'''

# 전체 제품 조회
def showProduct():
    sql = "SELECT * FROM Product"
    curs.execute(sql)

    result = curs.fetchall()

    productList.clear()
        
    for data in result :
        # 제품 정보 딕셔너리
        productInfo = {}
        
        productInfo['제품번호'] = data[0]
        productInfo['제품명'] = data[1]
        productInfo['가격'] = data[2]
        productInfo['수량'] = data[3]

        productList.append(productInfo)

    print(f'-------------------------------------------------------')
    print(f'제품번호\t제품명\t\t가격\t\t수량')
    print(f'-------------------------------------------------------')

    for item in productList:
        print(f'{item["제품번호"]}\t\t{item["제품명"]}\t\t{item["가격"]}\t\t{item["수량"]}')

# 제품 1개 조회
def showProductInfo(pCode):
    sql = "SELECT * FROM Product WHERE pCode = %s"
    curs.execute(sql, (pCode))

    result = curs.fetchone()

    print(f'-------------------------------------------------------')
    print(f'제품번호\t제품명\t\t가격\t\t수량')
    print(f'-------------------------------------------------------')

    print(f'{result[0]}\t\t{result[1]}\t\t{result[2]}\t\t{result[3]}')

# 제품 추가
def insertProduct():
    pCode = input("▶ 제품번호 : ")
    pName = input("▶ 제품명 : ")
    price = input("▶ 가격 : ")
    amount = input("▶ 수량 : ")
    
    sql = "INSERT INTO Product VALUES(%s, %s, %s, %s)"
    curs.execute(sql, (pCode, pName, price, amount))

    conn.commit()

    # 제품 정보 딕셔너리
    productInfo = {}

    productInfo['제품번호'] = pCode
    productInfo['제품명'] = pName
    productInfo['가격'] = price
    productInfo['수량'] = amount

    productList.append(productInfo)

    print(f'▶ {pCode} 제품이 추가되었습니다.')    

# 제품 정보 수정
def updateProduct(pCode):
    amount = input("▶ 제품 수량을 입력하세요 : ")

    # 데이터 수정
    sql = "UPDATE Product SET amount=%s WHERE pCode=%s"
    curs.execute(sql, (amount, pCode))

    conn.commit()

    print(f'▶ {pCode} 제품의 정보 수정이 완료되었습니다.')


# 제품 1개 삭제
def deleteProduct(pCode):
    sql = "DELETE FROM Product WHERE pCode=%s"
    curs.execute(sql, (pCode))

    conn.commit()

    print(f'▶ {pCode} 제품이 삭제되었습니다.')    

print()
print("###################################################")
print("            😎 제품 관리 프로그램 😎               ")
print("###################################################")

while True :
    print()
    sel = input("👩 메뉴를 선택하세요 => 전체제품보기(1), 제품검색(2), 제품추가(3), 제품수정(4), 제품삭제(5), 종료(exit) : ")

    if(sel == "1"):
        showProduct()
    elif(sel == "2"):
        print("♣ 제품 조회 ♣")
        pCode = input("▶ 검색할 제품번호 : ")
        showProductInfo(pCode)
    elif(sel == "3"):
        print("♣ 제품 추가 ♣")
        insertProduct()
    elif(sel == "4"):
        print("♣ 제품 수정 ♣")
        pCode = input("▶ 수정할 제품번호 : ")
        updateProduct(pCode)
    elif(sel == "5"):
        print("♣ 제품 삭제 ♣")
        pCode = input("▶ 삭제할 제품번호 : ")
        deleteProduct(pCode)        
    elif(sel == "exit"):
        print("###################################################")
        print("            😭 다음에 또 만나요 😭                 ")
        print("###################################################")
     
        # 데이터베이스 연결 종료
        conn.close()
        break
