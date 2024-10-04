#코드로 데이터베이스 연결하기
#주소, 아이디 패스워드, 등이 필요함
#charset을 안한다면 한글을 사용할 수 없음! 다깨져요
#db연결하기 
import pymysql
conn = pymysql.connect(host = 'localhost',  #conn을 암묵적으로 연결자로 칭함
                       user = 'root',
                       password = 'root',
                       db = 'ShopDB',     #다른 db를 가져오고 싶다면 해당칸의 이름을 변경해주세요! 
                       charset = 'utf8'
                       )

#커서만들기 : db의 결과를 돌려받는 통로, 결과를 저장하는 공간
curs = conn.cursor()  #등호가 하나라면 오른쪽의 결과를 왼쪽에 저장할래의 뜻임! 여기서 cur은 함수지요

#SQL 실행
# SQL = "SELECT * FROM Product"
# curs.execute(SQL)

#fetch~~() : 튜플로 출력
#모든 데이터 가져오기
# result = curs.fetchall()

# #result 타입확인
# print(type(result))  #튜플에있는 데이터 출력은 반복문을 돌려야함!

# #출력
# for data in result:
#     print(data)

#2줄의 데이터만 가져오기
# result = curs.fetchmany(2)

# for data in result:
#     print(data)

#1줄의 데이터만 가져오기
# result = curs.fetchone()

# print(result)

# result = curs.fetchall()
# print('데이터 출력:',result)
#추가1
# result = curs.fetchone()
# print('데이터 출력:',result) #none : 위에서 모두출력하여 커서에 남는 데이터가 없음
#추가2
# result = curs.fetchone()
# print('데이터 출력:',result)

# result = curs.fetchall()
# print('데이터 출력:',result)

#종료
# conn.close()

# +알파

#데이터 추가 - mySQL에서 새로고침이 이뤄져야함 : 아래에서 commit 실행
#라이브러리추가 - 연결자 생성 - 커서 생성
#sql실행 : insert는 commit필요
# sql = "INSERT INTO Product(pCode,pName,price,amount,manuf)VALUES('p0005','핸드폰',800000,5,'엘지')"
# curs.execute(sql)

# #commit실행
# conn.commit()

# conn.close()

#데이터 수정
#SQL문 실행
#sql = "UPDATE Product SET price=50000 WHERE pCode='p0003"
#curs.execute(sql)

#conn.commit()

#conn.close()

#result = curs.fetchall()
#print("데이터출력:",result)

#데이터 삭제
#sql = "delect from Product where pCode='p0005'"
#curs.execute(sql)

#conn.commit()

#conn.close()

#result = curs.fetchall()
#print("데이터 출력:",result)

#실습 1
# sql = "select * from Product Where price between %s and %s"
# curs.execute(sql, (500000, 1000000))
# result = curs.fetchall()
# print(result)

#실습 2
sql = (Decimal('30000.0000'), Decimal('35'))'
curs.execute(sql)

result = curs.fetchall()
print(result)