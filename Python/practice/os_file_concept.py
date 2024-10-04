import os 
import pickle 

# --------------------------------------------
# 1. os 기초 예제 
# 
# 1) os.path 이해하기 (os.path.exists, os.path.join, os.path)
# 2) os.listdir / os.makedir 해보기 
# 3) os.getcwd / os.changedir 해보기 
# --------------------------------------------

#파이썬이 현재 실행되는 위치
# print(os.getcwd())

# for elem in os.listdir():
#     #print(elem)
    
#     if os.path.isdir(elem):
#         print(f"<DIR\t\t{elem}")

#     elif "." in elem:
#         extenstion =  elem.split(".")[-1]
#         print(f"{extenstion} file\t\t {elem}")

# #디렉토리 생성
# def create_dir(directory_name):
#     if not os.path.exists(directory_name):
#         print(f"{directory_name} does not exists;")
#         os.makedirs(directory_name)
#     else:
#         print(f"{directory_name} is exists.")

# create_dir("hello")
# --------------------------------------------
# 2. file 기초 예제 
# 
# 1) open 이해하기 
# 2) 파일 읽기, 써보기 
# --------------------------------------------

#f = open("example.txt", "a+",encoding = "utf-8")
##wirte모드는(w, w+) 이전 내용을 모두 지우고 다시 엶, 기존파일 날라감 
# a 는 append 로 내용을 삭제없이 수정하고 싶은 경우 사용
# r 은 읽기모드
#파일이 없는 경우 생성하고 싶다면 +

# f = open("example.txt", "r",encoding = "utf-8")

# for i in range(1,101):
    #print(i)
    #f.write(str(i)+"\n") 
    # print(" ", file = f)
    # print("^ ^", file = f)
    # print("0w0 ~", file = f)
    
#     print(f.readline())
#     print(f.readline())
#     for line in f.readline():
#         print(line)
# f.close() 
#.close는 종료시 닫는 역할

# from time import time
# begin = time()

# f = open("example.txt", "w+",encoding = "utf-8")

# for i in range(10000000):
#     print(str(i)*10000, file = f)
# f.close()
# end = time()
# print(f"{end - begin} sec passed for making example.txt")
# --------------------------------------------
# 3. pickle 기초 예제 
# 
# 1) pickle.load() 해보기 
# 2) pickle.dump() 해보기 
# --------------------------------------------

d = [1,1,2,3]

#(이름, 파일명) 
# wb : 바이트를 쓴다!, rb : 바이트를 읽는다
#던져두기
pickle.dump(d,open("empty_dict.pickle","wb+"))

#가져오기
e = pickle.load(open("empty_dict.pickle","rb"))
print(e)

