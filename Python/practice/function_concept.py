# --------------------------------------------
# 1. 함수의 다양한 입력들 살펴보기 
#
# 1) input이 없는 함수 
# 2) input이 여러 개 있는 함수 
# 3) input이 정해지지 않은 갯수만큼 있는 함수 
# --------------------------------------------
import math

def pi():
    """원주율을 소숫점 두 자리까지 반환하는 함수
    """
    x = "{:.2f}".format(math.pi)
    
    return x

    #print가 없으면 출력되지 않음, return은 함수의 출력값을 가지고 있지만 보여주지않음
#pi()

def left_append(lst, elem): #elem :element 줄임말
    """lst의 왼쪽에 elem을 넣고, lst를 반환하는 함수 
    """
    lst.insert(0,elem)
    return lst

#left_append([5,1,2,3,4,],10)


def left_extend(lst, *elem):
    """lst의 왼쪽에 정해지지 않은 갯수의 elem을 넣고 lst를 반환하는 함수 
    """
    elem_list = list(elem)
    for j, i in enumerate(elem_list):
        lst.insert(j,i)

    return lst

left_extend([1,2,3,4,],5,6,4,83)

# --------------------------------------------
# 2. 함수의 call stack 알아보기 
# 
# 1) 아래 함수 b()를 실행할 때, 실행된 함수의 순서는?
# --------------------------------------------

# def a():
#     return pi()

# def b():
#     return a()

# 실행순서 : b() 호출
# a() > pi() > x > "{:.2f}".format(math.pi) > 출력 : 3.14

# --------------------------------------------
# 2) 아래 함수 c()를 실행할 때, 실행된 함수의 순서와 각 함수의 input은? 
# --------------------------------------------

# def c(lst):
#     print(lst[0])

#     return c(lst[1:]) 
    
# c(list(range(10)))

# 실행순서 : print(lst[0]) # 0
# return c(lst[1:]) # 1,2,3 ~ ,9
