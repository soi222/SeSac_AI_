gems = [3, 3, 1, 2, 3, 2, 2, 3, 3, 1]

# Q1
# gems 리스트에 1이 포함되어 있다면 True 출력
#방법 1
if 1 in gems:
 print(True)

#방법 2
for i in gems:
    if i == 1:
        print(True)
        break

# Q2
# 집계함수
# gems 리스트를 딕셔너리로 idx와 갯수로 나타내기
# 서현, count함수 : count할 리스트.count(갯수가 궁금한 값)

def gems_info():
    dic = {}
    for i in range(1,4):
        dic[i] = 0
        for j in gems:
            val = gems.count(i)
            dic[i] = val
    return print(f"gems info = {dic}")

# Q2 선생님ver.
gems_info = {1:0,
             2:0,
             3:0}
for gem in gems:
    gems_info[gem] += 1
#print(gems_info)

gems_info_lst = [0] * 4

for gem in gems:
    gems_info_lst[gem] += 1
#print(gems_info_lst)

## 리스트 컴프리헨션
"""
▶ 리스트 컴프리헨션 == 리스트 내포
리스트를 간단하고 빠르게 만들 수 있음
"""
# 예시1
# 1~100을 가진 리스트를 만들자
lst = [num for num in range(1, 101) if num % 2 == 0]
#print(lst)

# 예시2
nums = []
for _ in range(5):
    num = int(input())
    nums.append(num)
print("nums = ",nums)

#리스트 내포
nums = [int(input()) for _ in range(5)]

# 임시함수,lambda
nums = [[0,1],[2,2],[5,0]]
nums.sort(key = lambda x : x[1])
print(nums)

nums.sort(key = lambda x:-x[0])
print(nums)

#minmax
T = int(input())

for tc in range(T):
    N = int(input())
    nums = map(int, input().split())

#min, max 구하기
#선형 탐색 - 최댓값 갱신 - 최솟값 갱신

nums = [3,5,100,51,9,1]

#float("INF") : 파이썬에서 무한대
#여기서는 값을 최대/ 최소로 초기화 시키는 것을 의미
max_num = -float("INF")
min_num = float("INF")

for num in nums:
    if num > max_num:
        max_num = num
    else:
        min_num = num


print(max_num - min_num)

def my_sort(lst):
  n = len(lst)

  for i in range(n):
    for j in range(0, n-i-1):
      if lst[i] > lst[i+1]:
        lst[i], lst[i+1] = lst[i+1], lst[i]

  return lst

max_val = my_sort[-1]
min_val = my_sort[0]

print(max_val - min_val)
