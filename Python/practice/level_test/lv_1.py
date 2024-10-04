all_smallcase_letters = 'abcdefghijklmnopqrstuvwxyz'

# --------------------------------------------
# 1. list/tuple 기초 예제들 
# 
# a는 1,2,3이 들어간 튜플, 
# b는 a부터 z까지 모든 알파벳 소문자가 들어간 리스트가 되도록 만들어보세요. 
# b를 만들 때 위에 주어진 all_smallcase_letters와 for loop를 사용해도 좋고, 손으로 다 쳐도 좋습니다. 
# --------------------------------------------

# write your code here 
A = (1,2,3)

B = character = tuple(all_smallcase_letters)


# --------------------------------------------
# 2. dict 기초 예제 
# 
# 1) upper_to_lower : A:a, B:b, C:c
#
# upper_to_lower은 모든 대문자 알파벳(ex. A)을 key로 가지고, 대응하는 소문자 알파벳(ex. a)을 value로 가지는 dict입니다. 
# 위에서 만든 b와 for loop를 이용해서 upper_to_lower을 만들어보세요. 
# 
# 2) lower_to_upper
#
# upper_to_lower과 반대로 된 dict를 만들어보세요. 
# 
# 3) alpha_to_number
# 
# 소문자 알파벳 각각을 key, 몇 번째 알파벳인지를 value로 가지는 dict를 만들어보세요. 
# 위 all_smallcase_letters와 enumerate함수를 사용하세요. 
# 알파벳 순서는 1부터 시작합니다. ex) alpha_to_number['a'] = 1
# 
# 4) number_to_alphabet 
#
# 1부터 26까지의 수를 key로, 소문자, 대문자로 이뤄진 문자열 2개의 튜플을 value로 가지는 dict를 만들어보세요. 
# --------------------------------------------
# write your code here 
#1)
all_letters_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
all_letters = character = list(all_letters_str)
#print(all_letters)

upper_to_lower = {}
for x,y in enumerate(all_letters):
    for z,zz in enumerate(B):
        upper_to_lower[y] = zz
        if x == z:
            break
#print(upper_to_lower)

#2)
lower_to_upper = {}
for x,y in enumerate(all_letters):
    for z,zz in enumerate(B):
        lower_to_upper[zz] = y
        if x == z:
            break
#print(upper_to_lower)

 #3)
for i,j in enumerate(all_smallcase_letters):
    pass
    #print(f"alpha_to_number['{j}'] = {i+1}")

#4)1 = (A,a)
number_to_alphabet = {}
for x,y in enumerate(all_letters):
    for z,zz in enumerate(B):
        number_to_alphabet[x+1] = (y,zz)
        if x == z:
            break
#print(number_to_alphabet)

# --------------------------------------------
# 3. 주어진 문자열의 대소문자 바꾸기 
#
# 위 2에서 만든 dict들을 이용하여, 아래 문제들을 풀어보세요. 
#  
# 1) 주어진 문자열을 모두 대문자로 바꾼 문자열을 만들어보세요. 
# 2) 주어진 문자열을 모두 소문자로 바꾼 문자열을 만들어보세요. 
# 3) 주어진 문자열에서 대문자는 모두 소문자로, 소문자는 모두 대문자로 바꾼 문자열을 만들어보세요. 
# 4) 주어진 문자열이 모두 알파벳이면 True, 아니면 False를 출력하는 코드를 짜보세요. 
# --------------------------------------------

C = 'absdf123SAFDSDF'
C_list = character = list(C)
num = (1,2,3)

#1)
for idx,char in enumerate(C_list): 
    if char in B:
        change_big = ord(char) - 32
        C_list[idx]  = chr(change_big)
    
    elif char in num:
        pass

#print(C_list)

#2)
for idx,char in enumerate(C_list): 
    if char in all_letters: #대문자
        change_small = ord(char) + 32
        C_list[idx] = chr(change_small)


    elif char in num:
        pass

#print(C_list)

#2)

#3)
for idx,char in enumerate(C_list): 
    if char in all_letters: #대문자
        change_small = ord(char) + 32
        C_list[idx] = chr(change_small)

    elif char in B:
        change_big = ord(char) - 32
        C_list[idx]  = chr(change_big)
    
    elif char in num:
        pass

#print(C_list)

#4)
for idx,char in enumerate(C_list): 
    if char in all_letters and char in B: 
        #pass
        #print("True")
    
    else:
        pass
        #print("False")
        break


# --------------------------------------------
# 4. 다양한 패턴 찍어보기 
# 
# 1) 피라미드 찍어보기 - 1 
#
# 다음 패턴을 프린트해보세요. 
#
#     *
#    ***
#   *****
#  *******
# *********
# --------------------------------------------

# write your code here 

# floor = 5
# for i in range(floor):
#     for j in range(floor - i - 1):
#         print(" ", end = '')
#     for j in range(2 * i + 1):
#         print("*", end = '')
#     print()

# --------------------------------------------
# 2) 피라미드 찍어보기 - 2 
# 
# 다음 패턴을 프린트해보세요. 
# 
#     * 
#    * * 
#   * * * 
#  * * * * 
# * * * * * 
# --------------------------------------------

# write your code here 
# floor = 5
# for i in range(floor): #0,1,2,3,4
#     for j in range(floor - i - 1): #공백 넣기
#         print(" ", end = '')

#     for j in range(i + 1):#별 넣기
#         print("*", end = ' ')
#     print()
    
# --------------------------------------------
# 3) 피라미드 찍어보기 - 3 
# 
# 다음 패턴을 프린트해보세요. 
#
#     A 
#    A B 
#   A B C 
#  A B C D 
# A B C D E 
# --------------------------------------------

# write your code here 

floor = 5
alphabet = {0: "A", 1:"B", 2:"C", 3:"D", 4:"E"}

# for i in range(floor):
#     for j in range(floor - i - 1):
#         print(" ", end = "")
    
#     for al in range(i+1): 
#         print(alphabet[al], end = " ")
    
#     print()
# --------------------------------------------
# 4) 피라미드 찍어보기 - 4 
# 
# 다음 패턴을 프린트해보세요. 
# 
#       1 
#      1 1 
#     1 2 1 
#    1 3 3 1 
#   1 4 6 4 1
# --------------------------------------------

# write your code here 
#좌우는 모두 1이며, 중간 값은 위의 숫자를 더한 값

floor = 5
triangle = [[1]]

for i in range(1, floor):
    new = [1]

    for j in range(1,i):
        new.append(triangle[i-1][j-1] + triangle[i-1][j])
    new.append(1)
    triangle.append(new)

for k in range(floor):
    space = " " * (floor - k)
    values = map(str,triangle[k])
    result = " ".join(values)
#    print(f"{space}{result}")

# --------------------------------------------
# 5) 다음 패턴을 찍어보세요. 
# 
# *         *         * 
#   *       *       *   
#     *     *     *     
#       *   *   *       
#         * * *         
#           *           
#         * * *         
#       *   *   *       
#     *     *     *     
#   *       *       *   
# *         *         * 
# --------------------------------------------

# write your code here 
floor = 5

star = "* "
space = "  "

top_cell = []
for i in range(floor+1):
    top_cell.append(space * i + star + space * (floor - i) + star + space * (floor - i) + star)

for j in range(floor+1):
    pass
#    print(top_cell[j], end = "\n")

#print(space * (floor + 1) + star)

top_floor = []
for x in range(0, floor+1):
    top_floor.append(space * (floor - x) + star + space * x + star + space * x + star)

for y in range(floor+1):
    pass
#    print(top_floor[y], end = "\n")

