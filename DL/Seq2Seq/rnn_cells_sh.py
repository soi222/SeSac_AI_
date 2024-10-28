import torch
import torch.nn as nn

class RNNCellManual(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(RNNCellManual, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.in2hidden = nn.Linear(input_size, hidden_size)
        self.hidden2hidden = nn.Linear(hidden_size, hidden_size)

    def forward(self, x_time, h_time): # x 는 현재, h는 이전의 상태
        batch_size = x_time.size(0)
        h = torch.tanh(self.in2hidden(x_time) + self.hidden2hidden(h_time))

        return h
    
    def initialize(self, batch_size):
        return torch.zeros(batch_size, self.hidden_size)
    


class LSTMCellManual(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(LSTMCellManual, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        
        self.i2input = nn.Linear(input_size, hidden_size)
        self.h2input = nn.Linear(hidden_size, hidden_size)

        self.i2forget = nn.Linear(input_size, hidden_size)
        self.h2forget = nn.Linear(hidden_size, hidden_size)

        self.i2gate = nn.Linear(input_size, hidden_size)
        self.h2gate = nn.Linear(hidden_size, hidden_size)

        self.i2out = nn.Linear(input_size, hidden_size)
        self.h2out = nn.Linear(hidden_size, hidden_size)

    
    def forward(self, x, h, c):
        batch_size = x.size(0)
        assert x.size(1) == self.input_size
        
        assert h.size(0) == batch_size
        assert h.size(1) == self.hidden_size

        i_t = torch.sigmoid(self.i2input(x) + self.h2input(h))
        f_t = torch.sigmoid(self.i2forget(x) + self.h2forget(h))
        g_t = torch.tanh(self.i2gate(x) + self.h2gate(h))
        i_t = torch.sigmoid(self.i2out(x) + self.h2out(h))

        c_t = f_t * c_t + i_t * g_t
        h_t = o_t + torch.tanh(c_t)

        return h_t, c_t
    
    def initialize(self, batch_size):
        return torch.zeros(batch_size, self.hidden_size), torch.zeros(batch_size, self.hidden_size)
    