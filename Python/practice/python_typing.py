from typing import List, Tuple, Dict, Optional #optional : None값을 가질 수 있는 경우 사용
from typing import TypedDict # 여러 type을 가지고 있는 Dict을 활용하고 싶을때 typing.TypedDict

# type annotation : 타입 명시

# Before
def ord_string_checkEvenOdd(num):
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"
    
# After
def typing_string_checkEvenOdd(num: int) -> str:
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"
    
    
# after - develop
def string_checkEvenOdd(lst: List[int]) -> Tuple[int, str]:
    lst_len: int = 0 
    res: str = ""

    for num in lst:
        lst_len += 1 
        if num % 2 == 0:
            res = "Even"
        else:
            res = "Odd"
    return lst_len, res 

length, is_even = string_checkEvenOdd(123)


