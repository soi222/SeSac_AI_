"""
Todos 

- Vocab class 및 데이터 핸들링하는 코드 만들 것 (seq2seq 구조화.zip 참고)
- trainer 코드 만들 것 / evaluatation하는 코드 만들 것 
"""

import random 
import torch
import torch.nn as nn 

class RNNManual(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        self.i2h = nn.Linear(input_dim, hidden_dim)
        self.h2h = nn.Linear(hidden_dim, hidden_dim)
        self.input_dim = input_dim 
        self.hidden_dim = hidden_dim
    
    def forward(self, x, h):
        # x: (batch_size, input_dim)
        # h: (batch_size, hidden_dim)
        return torch.tanh(self.i2h(x) + self.h2h(h))

    def init_hidden(self):
        return torch.zeros(self.hidden_dim)

class RNNEncoder(nn.Module):
    def __init__(self, hidden_dim, source_vocab, embedding_dim):
        self.cell = RNNManual(embedding_dim, hidden_dim)
        self.embedding = nn.Embedding(source_vocab.vocab_size, embedding_dim)
        self.vocab = source_vocab
        self.hidden_dim = hidden_dim
    
    def forward(self, x):
        # x: (batch_size, source_seq_length, embedding_dim)
        batch_size, source_seq_length, vocab_size = x.size() 
        assert self.vocab.vocab_size == vocab_size
        
        hidden = self.cell.init_hidden()
        
        for t in range(source_seq_length):
            char = x[:, t] # char: (batch_size, 1, vocab_size)
            embedded = self.embedding(char).unsqueeze(1) # embedded: (batch_size, embedding_dim)
            hidden = self.cell(embedded, hidden) # hidden: (batch_size, hidden_dim)
            assert hidden.size() == (batch_size, self.hidden_dim)

        return hidden 
    
class RNNDecoder(nn.Module):
    def __init__(self, hidden_dim, target_vocab, embedding_dim):
   
        self.cell = RNNManual(embedding_dim, hidden_dim)
        self.embedding = nn.Embedding(target_vocab.vocab_size, embedding_dim)
        self.h2o = nn.Linear(hidden_dim, target_vocab.vocab_size)
        
        self.vocab = target_vocab
        self.hidden_dim = hidden_dim
        self.softmax = nn.LogSoftmax(dim = -1)

    def forward(self, encoder_last_hidden, teacher_forcing_ratio = 0.5):
        batch_size, encoder_hidden_dim = encoder_last_hidden.size()
        
        encoder_input = torch.tensor([self.vocab.SOS_IDX for _ in range(batch_size)]) 
        # encoder_input: (batch_size, 1)
        
        x = self.embedding(encoder_input)
        h = encoder_last_hidden
        flag = torch.tensor([False for _ in range(batch_size)])
        result = []
        t = 0

        while True:
            h = self.cell(x, h)
            y = self.h2o(h) # y: (batch_size, self.vocab.vocab_size)
            result.append(y)
            pred = torch.argmax(self.softmax(y)) # pred: (batch_size, ) / contains indices of vocab with the highest probability 

            if random() < teacher_forcing_ratio:
                x = x[:, t+1]
            else:
                x = self.embedding(y)

            check_eos = pred == self.vocab.EOS_IDX
            flag = flag or check_eos 
            t += 1 
            if all(flag) : break 

        
        return torch.stack(result, dim = 1) 

class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder):
        self.encoder = encoder
        self.decoder = decoder 

    def forward(self, x):
        encoder_last_hidden = self.encoder(x) 
        output = self.decoder(encoder_last_hidden)

        return output 
    







