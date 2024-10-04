#shopDB

import pymysql

conn = pymysql.connect(host = 'localhost', 
                       user = 'root',
                       password = 'root',
                       db = 'ShopDB',     
                       charset = 'utf8'
                       )

curs = conn.cursor()


print()
print("##########################################################")
print("                  ◎제품 관리 프로그램◎                    ")
print("##########################################################")
print()
print()

while True:

    lst = [0,]
    user_input = input("메뉴를 선택하세요 => 전체제품보기(1), 제품검색(2),제품추가(3), 제품수정(4), 제품삭제(5),종료(exit) : ")
    
    if user_input == "1":
        print()
        print("----------------------------------------------------------")
        print("제품번호   제품명       가격        수량     제조사  ")
        print("----------------------------------------------------------")

        curs.execute("SELECT * FROM product")

        sql = curs.fetchall()
        
        for product in sql:
            for i in lst:
                print(product[0],'    ',product[1],'    ',product[2],'    ',product[3],'    ',product[4])


    #제품검색
    elif user_input == "2":
        product_input = input("검색을 원하는 제품명을 입력하세요: ")
        sql = "select * from product where pName = %s;"
        
        curs.execute(sql, product_input)

        result = curs.fetchone()

        if result:
            print(result)
        else:
            print("해당 제품은 존재하지 않습니다.")

    #제품 추가
    elif user_input == "3":

        productid_input = input("추가하실 제품번호를 입력하세요: ")
        productname_input = input("추가하실 제품명을 입력하세요: ")
        productprice_input = input("추가하실 제품의 가격을 입력하세요: ")
        productamount_input = input("추가하실 제품의 수량을 입력하세요: ")
        productmanuf_input = input("추가하실 제품의 제조사를 입력하세요: ")

        sql = "INSERT INTO Product(pCode,pName,price,amount,manuf)VALUES(%s,%s,%s,%s,%s)"
        values = productid_input,productname_input,productprice_input,productamount_input,productmanuf_input
        
        curs.execute(sql, (values))
        
        conn.commit() #insert 후 임시저장임 > 이를 영구저장하기 위해 새로고침을 해주는 함수로 보면됨

        #conn.close() : 종료되면 while이 끝나여

        print("추가되었습니다")

    elif user_input == "4":
        modifyid_input = input("수정하고자 하는 제품번호를 입력해 주세요: ")
        modifyname_input = input("제품명을 수정해 주세요: ")


        sql = "UPDATE Product SET pCode = %s WHERE pName = %s"
        curs.execute(sql,(modifyid_input,modifyname_input))
        result = curs.fetchone()
        if result:
            print(result)
        else:
            print("해당 제품번호를 찾을 수 없습니다")
        conn.commit()

        #conn.close()
        print("수정되었습니다")

    #제품 삭제
    elif user_input == "5":
        delectname_input = input("삭제하고자 하는 제품명을 입력해 주세요: ")
        sql = "delete from Product where pName= %s"
        
        curs.execute(sql,(delectname_input,))
        conn.commit()

        #conn.close()
        print(f"{delectname_input}가 삭제되었습니다")

    #종료
    elif user_input == "6":
        print("종료되었습니다.")
        conn.close() # 데이터베이스 사용 종료  : 혹시 모를 사고를 대비하기 위함
        
        break
    






    