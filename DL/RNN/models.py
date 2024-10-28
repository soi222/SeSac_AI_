import torch 
import torch.nn as nn 
import torch.nn.functional as F 
import torch.optim as optim 

from debugger import debug_shell

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

class RecurrentNeuralNetwork(nn.Module):
    def __init__(self, hidden_size, alphabets, languages, batch_first = True):
        super(RecurrentNeuralNetwork, self).__init__()
        self.in2hidden = nn.Linear(len(alphabets), hidden_size)
        self.hidden2hidden = nn.Linear(hidden_size, hidden_size)
        self.hidden2out = nn.Linear(hidden_size, len(languages))

        self.hidden_size = hidden_size 
        self.batch_first = batch_first #batch_size = True :(batch_size, seq_length, features)

    def forward(self, x, hidden):
        # x: (batch_size, len(alphabets))
        assert len(x.shape) == 2, debug_shell()
        hidden = F.tanh(self.in2hidden(x) + self.hidden2hidden(hidden))

        if self.batch_first:
            out = self.hidden2out(hidden)
            out = F.log_softmax(out, dim = -1)
        else:
            out = F.log_softmax(self.hidden2out(hidden), dim = 0)

        assert len(out.shape) == 2, debug_shell()

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
                    print(f"[Epoch {epoch}, Step {num}] train loss : {mean_loss}, valid loss : {valid_loss}, valid accuarcy : {valid_acc}")

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

