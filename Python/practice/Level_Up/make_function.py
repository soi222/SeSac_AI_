import random 
import random
# --------------------------------------------
# 1. max / min 구현하기 
#
# cmp라는 함수를 이용한 min/max 구현하기. 
# cmp는 두 원소 중 더 큰 것을 반환하는 함수. : 우리반에서 가장 큰 사람을 고를꺼야(크다의 기준은 다양함 : 키, 몸무게 등등)
# 
# --------------------------------------------

#튜플로 만들기
lst_tuple = []
for i in range(1):
    for j in range(5):
        random_tuple = tuple(random.sample(range(100),2))
        lst_tuple.append(random_tuple)
#print(lst_tuple)

lst1 = [(1,5),(2,30),(15,98),(80,4)]

#기준 1 ) 튜플 first값이 가장 큰 값이 제일 큰 값이다
def max_value(lst):
    lst_max = []
    first_max = 0

    for i, (first,last) in enumerate(lst):
      if i == 0:
        first_max = first
        lst_max.append(lst[i])

      elif i > 0:
        if first + last > first_max:
          lst_max.clear()
          lst_max.append(lst[i])
          first_max = first

    return lst_max[0]

#max_value(lst_1)
#선생님 답 
lst = [(1,5),(2,3),(6,8),(9,5)]
def max_by_first_element(lst):
    max_elem = lst[0]

    for e in lst[1:]:
        if e[0] > max_elem[0]:
            max_elem = e
    return max_elem
print(max_by_first_element(lst))

def max_by_sum(lst):
    max_elem = lst[0]
    for e in lst[1:]:
        if sum(e) > sum(max_elem):
            max_elem = e
    return max_elem

#튜플 내 두 수 중에 큰 값을 반환하는 함수
def max_tuple_value(lst):
    lst_max_tuple = []
    first_sum = 0

    for i, (first,last) in enumerate(lst):
            if i == 0:
                first_sum = first + last
                lst_max_tuple.append(lst[i])

            elif i > 0:
                if first + last > first_sum:
                    lst_max_tuple.clear()
                    lst_max_tuple.append(lst[i])
                    first_sum = first + last

    return lst_max_tuple


#my_max
def my_max(lst, cmp = lambda x, y : x):  
  max_value = lst[0]

  for e in lst[1:]:
    if cmp(max_value,e) == e:
      max_value = e
      
    return e

#my_max(lst_1)

#my_max(lst_1, cmp = lambda x, y: x if sum(x) > sum(y) else y)
#my_max(lst_1, cmp = lambda x, y: x if x[0] > y[0] else y)





#2) min
def my_min(lst, cmp = lambda x, y : x):  
  min_value = lst[0]

  for e in lst[1:]:
    if cmp(e, min_value):
      min_value = e

  return min_value

#my_min(lst_tuple)
# my_min(lst1, cmp = lambda x, y: x if sum(x) < sum(y) else y)
# my_min(lst1, cmp = lambda x, y: x if x[0] < y[0] else y)
# --------------------------------------------
# 2. sort 구현하기 
# 
# 1) 그냥 순서대로 오름차순으로 정렬하기 
# 2) 오름차순, 내림차순으로 정렬하기 
# 3) 주어진 기준 cmp에 맞춰서 오름차순, 내림차순으로 정렬하기 
# 4) 주어진 기준 cmp가 큰 element를 출력하거나, 같다는 결과를 출력하게 만들기 
# 5) cmp상 같은 경우 tie-breaking하는 함수 넣기 
# --------------------------------------------
#1)
# def sort1(lst):
#     n = len(lst)
#     for i in range(n):
#       for j in range(0,n-i-1):
#         if lst[j] > lst[j+1]:
#           lst[j], lst[j+1] = lst[j+1], lst[j]

#     print(lst)
#lst1 = [1,5,6,8,4,2,19]
#sort1(lst1)
lst2 = [1,5,6,8,4,2,19]

def sort1(lst):
    res = []
    c = [e for e in lst]
    n = len(lst)
    while len(res) < n:
        res.append(my_min(lst, cmp = lambda x, y: min(x,y)))
        c.remove(my_min(lst, cmp = lambda x, y: min(x,y)))
    return res

#sort1(lst2)


# 2) 오름차순, 내림차순으로 정렬하기 
def sort2(lst, upper_to_lower = True):

    if upper_to_lower == True: #오름차순
        res = []
        c = [e for e in lst]
        n = len(lst)
        while len(res) < n:
            res.insert(0,(my_max(lst, cmp = lambda x, y: max(x,y))))
            c.remove(my_max(lst, cmp = lambda x, y: max(x,y)))
        return res
        

    elif upper_to_lower == False: #내림차순
        res = []
        c = [e for e in lst]
        n = len(lst)
        while len(res) < n:
            res.append(my_min(lst, cmp = lambda x, y: min(x,y)))
            c.remove(my_min(lst, cmp = lambda x, y: min(x,y)))
        return res


sort2(lst2,True)


#3)주어진 기준 cmp에 맞춰서 오름차순, 내림차순으로 정렬하기
def sort3(lst, upper_to_lower = True, cmp = lambda x, y: x):
    if upper_to_lower == True: #오름차순
        res = []
        c = [e for e in lst]
        n = len(lst)
        while len(res) < n:
            res.insert(0,(my_max(lst, cmp = lambda x, y: max(x,y))))
            c.remove(my_max(lst, cmp = lambda x, y: max(x,y)))
        return res

    elif upper_to_lower == False: #내림차순
        res = []
        c = [e for e in lst]
        n = len(lst)
        while len(res) < n:
            res.append(my_min(lst, cmp = lambda x, y: min(x,y)))
            c.remove(my_min(lst, cmp = lambda x, y: min(x,y)))
        return res

#4)주어진 기준 cmp가 큰 element를 출력하거나, 같다는 결과를 출력하게 만들기 
def sort4(lst, upper_to_lower = True, cmp = lambda x, y: x):
    max_value = lst[0]
    for e in lst[1:]:
        if cmp(max_value, e) == e:
            print(f"same value {e}")
            return max_value
        
        elif cmp(max_value, e) == e == max_value:
            print("same value")
            return e


#5) cmp상 같은 경우 tie-breaking하는 함수 넣기 
def sort5(lst, upper_to_lower=True, cmp=lambda x, y: x > y, tie_breaker=lambda x, y: random.choice([x, y])):
    n = len(lst)

    def demo_sort5(x, y):
        if cmp(x, y):
            return True
        elif cmp(y, x):
            return False
        else:
            return tie_breaker(x, y) == x

    for i in range(n):
        for j in range(0, n - i - 1):
            if upper_to_lower:
                if demo_sort5(lst[j], lst[j + 1]):
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
            else:
                if demo_sort5(lst[j + 1], lst[j]):
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]

    return lst
sort_lst = [(1, 4), (1, 5), (1, 2), (40, 24), (3, 1), (5, 4), (1, 3),(3,3)]
sort_lst_desc = sort5(
    sort_lst.copy(),
    upper_to_lower=True,
    cmp=lambda x, y: (x[0] > y[0]) or (x[0] == y[0] and x[1] > y[1]),
    tie_breaker=lambda x, y: random.choice([x, y])
)
print(f'내림차순: {sort_lst_desc}')
sort_lst_asc = sort5(
    sort_lst.copy(),
    upper_to_lower=True,
    cmp=lambda x, y: (x[0] < y[0]) or (x[0] == y[0] and x[1] < y[1]),
    tie_breaker=lambda x, y: random.choice([x, y])
)
print(f'오름차순: {sort_lst_asc}')


# --------------------------------------------
# os_file_concept.py 해보고 올 것 
# --------------------------------------------

# --------------------------------------------
# 3. safe pickle load/dump 만들기 
# 
# 일반적으로 pickle.load를 하면 무조건 파일을 읽어와야 하고, dump는 써야하는데 반대로 하면 굉장히 피곤해진다. 
# 이런 부분에서 pickle.load와 pickle.dump를 대체하는 함수 safe_load, safe_dump를 짜 볼 것.  
# hint. 말만 어렵고 문제 자체는 정말 쉬운 함수임.
# --------------------------------------------

def safe_load(pickle_path):
    pass 

def safe_dump(pickle_path):
    pass 


# --------------------------------------------
# 4. 합성함수 (추후 decorator)
# 
# 1) 만약 result.txt 파일이 없다면, 함수의 리턴값을 result.txt 파일에 출력하고, 만약 있다면 파일 내용을 읽어서 
#    '함수를 실행하지 않고' 리턴하게 하는 함수 cache_to_txt를 만들 것. txt 파일은 pickle_cache 폴더 밑에 만들 것.  
# 2) 함수의 실행값을 input에 따라 pickle에 저장하고, 있다면 pickle.load를 통해 읽어오고 없다면 
#    실행 후 pickle.dump를 통해 저장하게 하는 함수 cache_to_pickle을 만들 것. pickle 파일은 pickle_cache 폴더 밑에 만들 것. 
# 3) 함수의 실행값을 함수의 이름과 input에 따라 pickle에 저장하고, 2)와 비슷하게 진행할 것. pickle 파일은 pickle_cache 폴더 밑에, 각 함수의 이름을 따서 만들 것 
# --------------------------------------------

def cache_to_txt(function):
    

def cache_to_pickle(function):
    pass 
