import random
import torch
import torch.nn as nn

class RNNManual(nn.Module):
    def __init__(self, input_size, hidden_size):
        self.in2hidden = nn.Linear(input_size, hidden_size)
        self.hidden2hidden = nn.Linear(hidden_size, hidden_size)
        self.input_size = input_size
        self.hidden_size = hidden_size

        def forward(self, x, h): 
            # x : batch_size ,input_size
            # h(hidden_state) : batch_size, hidden_size
            return torch.tanh(self.in2hidden(x) + self.hidden2hidden(h))
        
        def init_hidden(self):
            return torch.zeros(self.hidden_size)
        
class RNN_Encoder(nn.Module):
    def __init__(self, hidden_size, source_vocab, embedding_size):
        self.cell = RNNManual(embedding_size, hidden_size)
        self.embedding = nn.Embedding(source_vocab.vocab_size, embedding_size) #source_vocab : 총 단어수
        self.vocab = source_vocab 
        self.hidden_size = hidden_size

    def forward(self, x): # x : 
        batch_size, source_seq_length, vocab_size = x.size()
        assert self.vocab.vocab_size == vocab_size

        hidden = self.cell.init_hidden()

        for t in range(source_seq_length):
            char = x[:, t]
            embedded = self.embedding(char).unsqueeze(1)
            hidden = self.cell(embedded, hidden)
            assert hidden.size() == (batch_size, self.hidden_size)


        
