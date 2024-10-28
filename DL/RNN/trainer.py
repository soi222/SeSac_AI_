import torch 
import torch.nn as nn 
import torch.nn.functional as F 
import torch.optim as optim 

import pickle

def train(model, train_data, 
            valid_data, 
            optimizer = optim.Adam, 
            criterion = F.nll_loss, 
            epochs = 100, 
            learning_rate = 0.001, 
            print_every = 1000):
    optimizer = optimizer(model.parameters(), lr = learning_rate)

    num = 0
    train_loss_lst = []
    valid_loss_lst = []

    #train 모델의 체크포인트마다 손실값과 정확도를 저장
    train_log = {}

    for epoch in range(epochs):
        for x, y in train_data:
            num += 1
            if isinstance(model, RecurrentNeuralNetwork):
                if model.batch_first:
                    x = x.transpose(0, 1)
                hidden = model.init_hidden()

                for char in x:
                    out, hidden = model(char, hidden) 
                       
            elif isinstance(model, FeedForwardNetwork):
                out = model(x)
            try:
                loss = criterion(out, y)

            except Exception:
                pickle.dump(train_data, open('train_data_error.pickle', 'wb+'))
                pickle.dump(valid_data, open('valid_data_error.pickle', 'wb+'))
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            mean_loss = torch.mean(loss).item()

            if num % print_every == 0 or num == 1:
                train_loss_lst.append(mean_loss)
                valid_loss, valid_acc = evaluate(model, valid_data)
                valid_loss_lst.append(valid_loss)

                print(f"[Epoch {epoch}, Step {num}] train loss : {mean_loss}, valid loss : {valid_loss}, valid acc : {valid_acc}")
                torch.save(model, f"checkpoints/feedforward_{num}.chkpts") 
                # chkpts : checkpoints, 주로 프로그래밍 상태나 데이터 저장 시점을 의미

                print(f"saved model to checkpoints/feedward_{num}.chkpts")
                train_log[f"checkpoints/feedforward_{num}.chkpts"] = [valid_loss, valid_acc]

    #train_log에 데이터 저장
    pickle.dump(train_log, open("checkpoints/train_log.dict", "wb+"))    

    return train_loss_lst, valid_loss_lst

def evaluate(model, data):
    model.eval()
    criterion = F.nll_loss

    cor, total = 0, 0
    loss_history = []
    with torch.no_grad():
        for x, y in data:
            if isinstance(model, RecurrentNeuralNetwork):
                if model.batch_first:
                    x = x.transpose(0, 1)
                hidden = model.init_hidden()
                for char in x:
                    out, hidden = model(char, hidden)    
            elif isinstance(model, FeedForwardNetwork):
                out = model(x)
            try:
                loss = criterion(out, y)
            except Exception:
                pickle.dump(data, open('valid_data_error.pickle', 'wb+'))
            loss = criterion(out, y)
            loss_history.append(torch.mean(loss).item())
            cor += torch.sum((torch.argmax(out, dim = 1) == y).float())
            total += y.size(0)
        return sum(loss_history) / len(loss_history), cor / total

if __name__ == '__main__':
    import os 

    from data_handler import generate_dataset 
    from models import RecurrentNeuralNetwork 
    
    train_dataloader, valid_dataloader, test_dataloader, alphabets_99, max_length, all_languages = generate_dataset()

    if 'train_data_error.pickle' in os.listdir():        
        train_dataloader = pickle.load(open('train_data_error.pickle', 'rb'))

    if 'valid_data_error.pickle' in os.listdir():        
        valid_dataloader = pickle.load(open('valid_data_error.pickle', 'rb'))
    
    rnn = RecurrentNeuralNetwork(128, alphabets_99, all_languages)
    train_loss_history, valid_loss_history = train(rnn, train_dataloader, valid_dataloader, epochs = 1)
