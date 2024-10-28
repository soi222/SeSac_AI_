import tensor
import random
  
"""
zeros = torch.zeros((2, 3))
ones = torch.ones((2, 3))
rand = torch.rand((2, 3))
eye = torch.eye(3)  # 3x3 Identity matrix
normal = torch.randn((2, 3))  # Normal distribution
arange_tensor = torch.arange(start=0, end=10, step=2) # range(0, 10, 2)
linspace_tensor = torch.linspace(start=0, end=1, steps=5) # 0 0.25 0.5 0.75 1
"""
  
## 위의 함수를 torch.tensor와 리스트 operation을 이용해 구현하라

def nested_list(shape, value):
    if len(shape) == 1:
        l = shape[0]
    return [value for _ in range(l)]
      
  else:
    l = shape[0]
    return [nested_list(shape[1:], value = value) for _ in range(l)]

def random_integer(low, high):
    return random.randn(low, high)
      
def random_nested_list(shape, smaple_from, *args):
    if len(shape) == 1:
        l = shape[0]
    return [sample_from(*args) for _ in range(l)]

    else:
          l = shape[0]
    return [random_nested_list(shape[1:], random_integer(*args)for _ in range(l)]


def zeros(shape):
    return nested_list(shape, value = 0) 

def ones(shape):
    return nested_list(shape, value = 1)

def rand(shape):
    return random_nested_list(shape,random.random)

def randn(shape):
    return random_nested_list(shape, random.guass, 0, 1)

def eyes(num):
    res = []
    for i in range(num):
        lst = []
        for j in range(num):
              lst.append(0.)
    res.append(lst)

    for i in range(num):
        res[i][i] = 1.
    return res
                               

## linear_regression
def Generate_data(true_w, true_b, data_n, noise):
    X = torch.randn(data_n, 1) * 10
    y = true_w * X + true_b + torch.randn(data_n, 1) * noise
    return X, y

def linear_regression(ture_w, true_b, data_n, val = 10, noise = 0.2):
    X, y = Generate_data(ture_w, true_b,data_n = data_n, noise = noise)
    
    w = torch.randn(1, 1, requires_grad = True)
    b = torch.randn(1, requires_grad = True)                           

    learning_rate = 0.005
    epochs = 1000
                               
    for epoch in range(epochs):
        y_pred = w * X + b
        loss = torch.mean((y_pred - y) ** 2) #왜 제곱을 하지?

        loss.backward()
        with torch.no_grad():
            w -= learning_rate * w.grad
            b -= learning_rate * b.grad
                               
        w.grad.zero_()
        b.grad.zero_()
        print(f"Epoch {epoch} : w = {w.item():.4f}, b = {b.item():.4f}, loss = {loss.item():.4f}")

Generate_data(0.2, 0.3,10, 0.2)
linear_regression(0.2,0.3,10)
