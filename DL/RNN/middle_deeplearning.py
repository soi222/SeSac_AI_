# defaultdict 설명

from collections import defaultdict

d = defaultdict(int)

for i in range(10):
    d[i] += 1
#print(d) #defaultdict(<class 'int'>, {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1})

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import glob
import matplotlib.pyplot as plt
import random

from collections import defaultdict
from torch.utils.data import DataLoader, TensorDataset
import random
import pickle
import os

OOV = '[OOV]'
PAD = '[PAD]'

# hyperparameters
batch_size = 32

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

# for batch_x, batch_y in dataset:
#     for i in range(batch_x.size(0)):
#         print(tensor2word(batch_x[i], alphabets), idx2lang(batch_y[i], languages))
#     break


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

    train_dataloader = DataLoader(train_dataset, batch_size = batch_size, shuffle= True)
    valid_dataloader = DataLoader(valid_dataset, batch_size = batch_size, shuffle= True)
    test_dataloader = DataLoader(test_dataset, batch_size = batch_size, shuffle= True)

    return train_dataloader, valid_dataloader, test_dataloader, alphabets_99, max_length, all_languages

train_dataloader, valid_dataloader, test_dataloader, alphabets_99, max_length, all_languages  = generate_dataset()

def modify_dataset_for_ffn(dataset):
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
    
        
def plot_loss_history(loss_history_name, other_loss_history_name, loss_history, other_loss_history = []):
    plt.plot(range(1, len(loss_history) + 1), loss_history)
    
    if other_loss_history != []:
        plt.plot(range(1, len(other_loss_history) + 1), other_loss_history)
        plt.show()


class FeedForwardNetwork(nn.Module):
    def __init__(self, hidden_size, alphabets_99, max_length, languages):
        super(FeedForwardNetwork, self).__init__()
        self.layer1 = nn.Linear(len(alphabets_99) * max_length, hidden_size)
        self.layer2 = nn.Linear(hidden_size, len(languages))

    def forward(self, x):
        # x : (batch_size, max_length, len(alphabets) : 32, 12, 57)
        #print(f"forward input shape is {x.shape}") # X.shape : [32, 384]

        out = self.layer1(x)
        out = F.relu(out)
        out = self.layer2(out)
        out = F.log_softmax(out, dim = -1)

        return out
    
    def train_model(self, train_data, valid_data, epochs = 100, learning_rate = 0.001, print_every = 1000):
        criterion = F.nll_loss
        optimizer = optim.Adam(self.parameters(), lr = learning_rate)

        num = 0
        train_loss_lst = []
        valid_loss_lst = []

        #train 모델의 체크포인트마다 손실값과 정확도를 저장
        train_log = {}

        for epoch in range(epochs):
            for x, y in train_data:
                num += 1
                y_pred = self(x)
                loss = criterion(y_pred, y)

                loss.backward()
                optimizer.step()
                optimizer.zero_grad()

                mean_loss = torch.mean(loss).item()

                if num % print_every == 0 or num == 1:
                    train_loss_lst.append(mean_loss)
                    valid_loss, valid_acc = self.evaluate(valid_data)
                    valid_loss_lst.append(valid_loss)

                    print(f"[Epoch {epoch}, Step {num}] train loss : {mean_loss}, valid loss : {valid_loss}, valid acc : {valid_acc}")
                    torch.save(self, f"checkpoints/feedforward_{num}.chkpts") 
                    #chkpts : checkpoints, 주로 프로그래밍 상태나 데이터 저장 시점을 의미

                    print(f"saved model to checkpoints/feedward_{num}.chkpts")
                    train_log[f"checkpoints/feedforward_{num}.chkpts"] = [valid_loss, valid_acc]

        #train_log에 데이터 저장
        pickle.dump(train_log, open("checkpoints/train_log.dict", "wb+"))    

        return train_loss_lst, valid_loss_lst

    def evaluate(self, data):
        self.eval()
        criterion = F.nll_loss

        cor, total = 0, 0
        loss_history = []
        with torch.no_grad():
            for x, y in data:
                y_pred = self(x)
                loss = criterion(y_pred, y)
                loss_history.append(torch.mean(loss).item())
                cor += torch.sum((torch.argmax(y_pred, dim = 1) == y).float())
                total += y.size(0)
            return sum(loss_history) / len(loss_history), cor / total

#test

dataset = train_dataloader
train_data, valid_data, test_data = modify_dataset_for_ffn(dataset)


# model = FeedForwardNetwork(32, alphabets_99, max_length, languages)
# loss, acc = model.evaluate(train_data)

# train_loss_history, valid_loss_history = model.train_model(train_data, valid_data)

# plot_loss_history("train_loss_history", "valid_loss_history", train_loss_history, valid_loss_history)


def find_best_model():
    train_log = pickle.load(open("checkpoints/train_log.dict", "rb"))
    tmp = []

    for k, freq in train_log.items():
        tmp.append((k, freq))

    path_model = max(tmp, key = lambda x : x[1][1])[0]

    return torch.load(path_model)


# model = find_best_model()
# model.evaluate(test_data)


class RecurrentNeuralNetwork(nn.Module):
    def __init__(self, hidden_size, alphabets, languages,  batch_first = True):
        super(RecurrentNeuralNetwork, self).__init__()
        self.in2hidden = nn.Linear(len(alphabets), hidden_size)
        self.hidden2hidden = nn.Linear(hidden_size, hidden_size)
        self.hidden2out = nn.Linear(hidden_size, len(languages))

        self.hidden_size = hidden_size 
        self.batch_first = batch_first #batch_first = True :(batch_size, seq_length, features)

    def forward(self, x, hidden):
        # x: (batch_size, max_length, len(alphabets))
        hidden = F.tanh(self.in2hidden(x) + self.hidden2hidden(hidden))

        if self.batch_first:
            out = self.hidden2out(hidden)
            out = F.log_softmax(out, dim = -1)

        else:
            out = F.log_softmax(self.hidden2out(hidden), dim = 0)

        return out, hidden

    def init_hidden(self):
        return torch.zeros(self.hidden_size)

    def train_model(self, train_data, valid_data, epochs = 100, learning_rate = 0.001, print_every = 1000):
        criterion = F.nll_loss
        optimizer = optim.Adam(self.parameters(), lr = learning_rate)

        num = 0
        train_loss_lst = []
        valid_loss_lst = []
        
        for epoch in range(epochs):
            for x, y in train_data:
                num += 1

                if self.batch_first:
                    x = x.transpose(0, 1)

                hidden = self.init_hidden()
                for char in x:
                    out, hidden = self(char, hidden)

                loss = criterion(out, y)

                loss.backward()
                optimizer.step()
                optimizer.zero_grad()

                mean_loss = torch.mean(loss).item()

                if num % print_every == 0 or num == 1:
                    train_loss_lst.append(mean_loss)
                    valid_loss, valid_acc = self.evaluate(valid_data)
                    valid_loss_lst.append(valid_loss)
                    print(f"[Epoch {epoch}, Step {num}] train loss : {mean_loss}, valid loss : {valid_loss}, valid accuarcy :{valid_acc}")

        print(f"accuarcy : {valid_acc:.4f}")

        return train_loss_lst, valid_loss_lst


    def evaluate(self, data):
        self.eval()
        criterion = F.nll_loss

        cor, total = 0, 0
        loss_history = []
        with torch.no_grad():
            for x, y in data:
                if self.batch_first:
                    x = x.transpose(0, 1)

                hidden = self.init_hidden()
                for char in x:
                    out, hidden = self(char, hidden)
                if len(out.size()) != 2:
                    print(x.shape)
                    print(out.shape)
                    print(y.size())
                loss = criterion(out , y)

                loss_history.append(torch.mean(loss).item())
                cor += torch.sum((torch.argmax(out, dim = 1) == y).float())
                total += y.size(0)

        return sum(loss_history) / len(loss_history), cor/total

from debugger import debug_shell
debug_shell()
# train_dataset, valid_dataset, test_dataset, alphabets, max_length, languages  = generate_dataset()

# rnn = RecurrentNeuralNetwork(128, alphabets_99, all_languages)
# train_loss_history, valid_loss_history = rnn.train_model(train_dataset, valid_dataset)

#plot_loss_history(train_loss_history, valid_loss_history, train_loss_history, valid_loss_history)

