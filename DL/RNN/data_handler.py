import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import glob
import matplotlib.pyplot as plt
import random
import numpy as np

from collections import defaultdict
from torch.utils.data import DataLoader, TensorDataset
import random
import pickle
import os

OOV = '[OOV]'
PAD = '[PAD]'


def word2tensor(word, max_length, alphabets, pad = PAD, oov = OOV):
    # return torch.tensor with size (max_length, len(alphabets))
    res = torch.zeros(max_length, len(alphabets))

    for idx, char in enumerate(word):
        if idx < max_length:
            # alphabets에 있는 문자면 변환, 없으면 oov로 처리
            if char in alphabets:
                res[idx] = letter2tensor(char, alphabets, oov = oov)
            else:
                res[idx] = letter2tensor(oov, alphabets, oov = oov)

    # 나머지 padding 처리
    for i in range(max_length - len(word)):
        res[len(word) + i] = letter2tensor(pad, alphabets, oov = oov)

    return res

def letter2tensor(letter, alphabets, oov = OOV):
    res = [0 for _ in range(len(alphabets))]

    if letter in alphabets:
        idx = alphabets.index(letter)
    else:
        idx = alphabets.index(oov)

    res[idx] = 1

    return torch.tensor(res)

def determine_alphabets(data, pad = PAD, oov = OOV, threshold = 0.999):
    charNnum = []
    char_dict = defaultdict(int)

    for local_name, languages in data:
        for char in local_name:
            char_dict[char.lower()] += 1
    
    for chr, num in char_dict.items():
        charNnum.append((chr, num))

    charNnum = sorted(charNnum, key = lambda x:x[1], reverse = True)
    total_count = sum([e[1] for e in charNnum])
    s = 0

    local_alphabets = []

    for chr2, num2 in charNnum:
        s += num2
        if s < threshold * total_count:
            local_alphabets.append(chr2)

    local_alphabets.append(pad)
    local_alphabets.append(oov)

    return local_alphabets

def determine_max_length(data, threshold = 0.99):
    lst = []
    name_leng_dict = defaultdict(int)

    for local_name, language in data:
        name_leng_dict[len(local_name)] += 1

    for idx, num in name_leng_dict.items():
        lst.append((idx, num))

    lst = sorted(lst, key= lambda x:x[1], reverse = True)
    total_count = sum([e[1] for e in lst])
    s = 0

    for char, numb in lst:
        s += numb
        if s > threshold * total_count:
            return char - 1

    return max(lst, key = lambda x:x[0])[0]
    
def load_file():
    files = glob.glob('C:/Users/user/Desktop/DL/names/*.txt')

    assert len(files) == 18

    f_data = []
    f_languages = []

    for file in files:
        with open(file) as f:
            names = f.read().strip().split("\n")
            language = file.split("\\")[1].split(".")[0]

        if language not in f_languages:
            f_languages.append(language)
        
        for local_name in names:
            f_data.append([local_name, language])

    return f_data, f_languages

#model학습
def split_train_valid_test(x, y, train_valid_test_ratio = (0.7, 0.15, 0.15)):
    # TensorDataset -> TensorDataset, TensorDataset, TensorDataset
    # x, y: list of data
    train_ratio, valid_ratio, test_ratio = train_valid_test_ratio
    y_dict = defaultdict(int)

    for y_data in y:
        y_dict[y_data.item()] += 1

    no_per_label = {} # y_label별 각각 train, valid, test

    for y_label, freq in y_dict.items():
        train_size, valid_size, test_size = int(freq * train_ratio), int(freq * valid_ratio), freq - int(freq * train_ratio) - int(freq * valid_ratio)
        no_per_label[y_label] = [train_size, valid_size, test_size]
    
    train_x, train_y = [], []
    valid_x, valid_y = [], []
    test_x, test_y = [], []

    for x_data, y_data in zip(x,y):
        idx = pick_train_valid_test(*no_per_label[y_data.item()])
        assert no_per_label[y_data.item()][idx] > 0
        no_per_label[y_data.item()][idx] -= 1

        if idx == 0:
            train_x.append(x_data)
            train_y.append(y_data)

        elif idx == 1:
            valid_x.append(x_data)
            valid_y.append(y_data)
        
        elif idx == 2:
            test_x.append(x_data)
            test_y.append(y_data)

    return train_x, train_y, valid_x, valid_y, test_x, test_y

def pick_train_valid_test(train, valid, test):
    assert [train, valid, test] != [0, 0, 0]
    options = [train, valid, test]

    pick = random.choice([0, 1, 2])

    while options[pick] == 0:
        pick = random.choice([0,1,2])

    assert options[pick] != 0
    return pick

def tensor2word(ten, alphabets):
    #t.shape : max_length, len(alphabets)
    result = []
    for char_tensor_ver in ten:
        char = alphabets[int(torch.argmax(char_tensor_ver).item())]
        result.append(char)

    return result

def idx2lang(idx, languages):
    return languages[idx]

def generate_dataset(batch_size = 32, pad = PAD, oov = OOV):
    all_nameNleng, all_languages = load_file()

    alphabets_99 = determine_alphabets(all_nameNleng, pad = pad, oov = oov)
    max_length = determine_max_length(all_nameNleng)

    for idx, elem in enumerate(all_nameNleng):
        tmp = []
        for char in elem[0]:
            if char.lower() in alphabets_99:
                tmp.append(char.lower())
            else:
                tmp.append(oov)

        all_nameNleng[idx][0] = word2tensor(tmp, max_length, alphabets_99, pad = pad, oov = oov)
        assert all_nameNleng[idx][0].size(0) == max_length
        all_nameNleng[idx][1] = all_languages.index(all_nameNleng[idx][1])

    x = [e[0] for e in all_nameNleng]
    y = [torch.tensor(e[1]) for e in all_nameNleng]

    train_x, train_y, valid_x, valid_y, test_x, test_y = split_train_valid_test(x, y)

    train_x = torch.stack(train_x)
    train_y = torch.stack(train_y)
    valid_x = torch.stack(valid_x)
    valid_y = torch.stack(valid_y)
    test_x = torch.stack(test_x)
    test_y = torch.stack(test_y)

    train_dataset = TensorDataset(train_x, train_y)
    valid_dataset = TensorDataset(valid_x, valid_y)
    test_dataset = TensorDataset(test_x, test_y)

    train_dataloader = DataLoader(train_dataset, batch_size = batch_size, shuffle = True)
    valid_dataloader = DataLoader(valid_dataset, batch_size = batch_size, shuffle = True)
    test_dataloader = DataLoader(test_dataset, batch_size = batch_size, shuffle = True)

    return train_dataloader, valid_dataloader, test_dataloader, alphabets_99, max_length, all_languages

def modify_dataset_for_ffn(dataset, batch_size = 32):
    x = []
    y = []

    for batch_x, batch_y in dataset:
        
        # print('batch_x.shape is', batch_x.size())
        # print(batch_x)

        # print('batch_y.shape is', batch_y.size())
        # print(batch_y)
        
        for i in range(batch_x.size(0)): 
            x.append(batch_x[i].reshape((batch_x.size(2) * batch_x.size(1)))) 
            y.append(batch_y[i])

    train_x, train_y, valid_x, valid_y, test_x, test_y = split_train_valid_test(x, y)

    train_x = torch.stack(train_x)
    train_y = torch.stack(train_y)
    valid_x = torch.stack(valid_x)
    valid_y = torch.stack(valid_y)
    test_x = torch.stack(test_x)
    test_y = torch.stack(test_y)

    train_dataset = TensorDataset(train_x, train_y)
    valid_dataset = TensorDataset(valid_x, valid_y)
    test_dataset = TensorDataset(test_x, test_y)

    train_dataloader = DataLoader(train_dataset, batch_size = batch_size, shuffle = True)
    valid_dataloader = DataLoader(valid_dataset, batch_size = batch_size, shuffle = True)
    test_dataloader = DataLoader(test_dataset, batch_size = batch_size, shuffle = True)

    return train_dataloader, valid_dataloader, test_dataloader

if __name__ == '__main__':
    train_dataloader, valid_dataloader, test_dataloader, alphabets_99, max_length, all_languages  = generate_dataset()

    print(alphabets_99)
    print(max_length) 
    print(all_languages)

    for x, y in train_dataloader:
        print(x.shape)
        print(y.shape) 
        break 