def get_shape(lst):
    res = []
    cur = lst

    while isinstance(cur, list):
        res.append(len(cur))
        cur = cur[0]

    return res

def get_shape(lst):
    if not isinstance(lst, list):
        return []
    else:
        shapes = []
        for elem in lst:
            shape = get_shape(elem)
            if shape not in shapes:
                shapes.append(shape)
        if len(shapes) == 1:
            return [len(lst)] + get_shape(lst[0])
        else:
            return False

def fill(l, r):
    """If len(l) > len(r), fill 1 to r's front, so that len(l) == len(r),
    If len(r) < len(l), do the opposite.
    """
    if len(l) > len(r):
        diff = len(l) - len(r)
        r = [1 for _ in range(diff)] + r
        return l, r
    elif len(l) < len(r):
        diff = len(r) - len(l)
        l = [1 for _ in range(diff)] + l
        return l, r
    return l, r

def expand_dimension(l, dim_idx, r_s): #(lst, m, n ): (초기 리스트, 확장할 차원, n개의 갯수로 늘리겠다는 의)
    """
    l = [[1,2,3,]] (shape 1, 3)
    dim_idx = 0
    r_s = 4
    expand_dimension(l, 0, 4)
    >> [[1,2,3,], [1,2,3,], [1,2,3,], [1,2,3,]]

    l = [[[1,2,3]], [[1,2,3]], [[1,2,3]]] (shape 3, 1, 3 -> 3, 2, 3) #여기서 1차원은 초록색 괄호
    l[0] = [[1,2,3]], l[1], l[2] (shape 2, 3)
    dim_idx = 1
    r_s = 2
    expand_dimension(l, 1, 2)
    >> [[[1,2,3], [1,2,3]], [[1,2,3], [1,2,3]], [[1,2,3], [1,2,3]]] (shape 3, 2, 3)

    l / shape 4, 3, 2, 1, 2 -> 4, 3, 2, 5, 2
    expand_dimension(l, 3, 5)
    l[0], l[1], l[2], l[3] / shape 3, 2, 1, 2 -> 3, 2, 5, 2
    expand_dimension(l[0], 2, 5)
    expand_dimension(l[1], 2, 5)
    expand_dimension(l[2], 2, 5)
    expand_dimension(l[3], 2, 5)
    """

    assert get_shape(l)[dim_idx] == 1, (get_shape(l), dim_idx)

    if dim_idx == 0:
        return [l[0] for _ in range(r_s)]
    else:
        return [expand_dimension(e, dim_idx - 1, r_s) for e in l]


def broadcasting(l, r):
    shape_l = get_shape(l)
    shape_r = get_shape(r)

    assert shape_l and shape_r

    # 차원의 맞추기: 두 텐서의 차원(Dimension) 수가 다를 때,
    # 차원이 작은 텐서의 앞쪽에 1을 추가하여 차원을 맞춥니다.

    # (2, 3) / (4, 5, 2, 3) -> (1, 1, 2, 3) / (4, 5, 2, 3)

    l_is_bigger = False
    r_is_bigger = False
    diff = abs(len(shape_l) - len(shape_r))

    if len(shape_l) > len(shape_r):
        l_is_bigger = True
    elif len(shape_l) < len(shape_r):
        r_is_bigger = True

    shape_l, shape_r = fill(shape_l, shape_r)

    for _ in range(diff):
        if l_is_bigger:
            r = [r]  # r.shape: a1, a2, ... , an / [r].shape : 1, a1, a2, ... , an
        elif r_is_bigger:
            l = [l]

    assert shape_l == get_shape(l)
    assert shape_r == get_shape(r)

    # 크기 맞추기: 각 차원에서 크기가 1인 텐서는
    # 해당 차원의 크기를 큰 텐서의 크기에 맞춰 늘릴 수 있습니다.

    dim_idx = 0

    for l_s, r_s in zip(shape_l, shape_r):
        if l_s != r_s:
            if min(l_s, r_s) == 1:
                if l_s == 1:
                    l = expand_dimension(l, dim_idx, r_s)
                else: # r_s == 1
                    r = expand_dimension(r, dim_idx, l_s)
            else:
                return False
        dim_idx += 1

    return l, r

l = [[[1,2,3]], [[1,2,3]], [[1,2,3]]]
print("get_shape(I) :", get_shape(l))

r = [[1,2,3,], [1,2,3,], [1,2,3,], [1,2,3,]]
print(get_shape(r))

# 3 1 3 / 4 3 -> 3 1 3 / 1 4 3 -> 3 1 3 / 3 4 3 -> 3 4 3 / 3 4 3
# r = [[[1,2,3,], [1,2,3,], [1,2,3,], [1,2,3,]]]
r_ans = [[
            [1,2,3,],
            [1,2,3,],
            [1,2,3,],
            [1,2,3,]
          ],
         [[1,2,3,], [1,2,3,], [1,2,3,], [1,2,3,]],
         [[1,2,3,], [1,2,3,], [1,2,3,], [1,2,3,]]]

l_ans = [[[1,2,3], [1,2,3], [1,2,3], [1,2,3]],
         [[1,2,3], [1,2,3], [1,2,3], [1,2,3]],
         [[1,2,3], [1,2,3], [1,2,3], [1,2,3]]]

l, r = broadcasting(l, r)
print(get_shape(l), get_shape(r))
print(l_ans == l, r_ans == r)
