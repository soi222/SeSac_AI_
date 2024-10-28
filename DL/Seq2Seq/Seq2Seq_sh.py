import random 
import torch 
import torch.nn as nn 

class EncoderState:
    def __init__(self, **kargs):
        for k, v in kargs.items():
            exec(f'self.{k} = v')

    def initialize(self):
        assert "model_type" in dir(self)
        return self.model_type.initialize()
    

class Encoder(nn.Module):
    def __init__(self, source_vocab, embedding_size, hidden_size, model_type):
        super(Encoder, self).__init__()
        self.source_vocab = source_vocab
        self.embedding_size = embedding_size
        self.hidden_size = hidden_size
        self. model_type = model_type

        self.embedding = nn.Embedding(source_vocab.vocab_size, embedding_size) #nn.Embedding(num_embeddings : 임베딩을 할 단어들의 개수, embedding_dim)
        self.cell = model_type(embedding_size, hidden_size) 
        #model_type : cell의 종류 선택 (lstm ,rnn ..)


    def forward(self, seq_source): #source : 입력될 시퀀스 
        batch_size, seq_length = seq_source.size()

        embedded = self.embedding(seq_source) 
        #embedded : embedding을 지난 source로 텐서로 형성 (batch_size, seq_length, embedding_dim)의 형태로 지정
        encoder_state = self.cell.initialize(batch_size)

        from rnn_cells_sh import RNNCellManual, LSTMCellManual

        for t in range(seq_length):
            x_t = embedded[:, t, :]
            if self.model_type == RNNCellManual:
                encoder_state == self.cell(x_t, encoder_state)
            elif self.model_type == LSTMCellManual:
                encoder_state = self.cell(x_t, *encoder_state)

        return encoder_state


class Decoder(nn.Module):
    def __init__(self, target_vocab, embedding_size, hidden_size, model_type):
        super(Decoder, self).__init__()

        self.target_vocab = target_vocab
        self.embedding_size = embedding_size
        self.hidden_size = hidden_size
        self.model_type = model_type

        self.embedding = nn.Embedding(target_vocab.vocab_size, embedding_size)
        self.cell = model_type(embedding_size, hidden_size)
        self.h2out = nn.Linear(hidden_size, target_vocab.vocab_size)

    def forward(self, target, encoder_last_state, teacher_forcing_ratio = 0.5):
        batch_size, seq_length = target.size()

        outputs = []
        from rnn_cells_sh import RNNCellManual, LSTMCellManual

        input = torch.tensor([self.target_vocab.SOS_IDX for _ in range(batch_size)])
        decoder_state = encoder_last_state

        for time in range(seq_length):
            embeded = self.embedding(input)
            if self.model_type == RNNCellManual:
                decoder_state = self.cell(embeded, decoder_state) #현재값 embeded, 이전값 decoder_state를 입력받아 decoder_state에 저장
            elif self.model_type == LSTMCellManual:
                decoder_state = self.cell(embeded, *decoder_state)
            
            output = self.h2out(decoder_state)
            outputs.append(output)

            if random.random() < teacher_forcing_ratio and time < seq_length - 1:
                input = target[:, time+1]

            else:
                input = torch.argmax(output, dim = 1)
        return torch.stack(outputs, dim = 1)

class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder):
        super(Seq2Seq, self).__init__()
        self.encoder = encoder
        self.decoder = decoder

    def forward(self, source, target):
        encoder_hidden = self.encoder(source)
        outputs = self.decoder(target, encoder_hidden)

        return outputs
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    from data_handler_sh import parse_file 
    from rnn_cells_sh import RNNCellManual, LSTMCellManual

    embedding_dim = 256
    batch_size = 32
    encoder_model = RNNCellManual
    decoder_model = RNNCellManual
    hidden_dim = 128
    criterion = nn.CrossEntropyLoss
    optimizer = torch.optim.Adam 
    learning_rate = 0.001 
    num_epochs = 10 

    (train, valid, test), source_vocab, target_vocab = parse_file('kor.txt', batch_size = batch_size)
    encoder = Encoder(source_vocab, embedding_dim, hidden_dim, encoder_model)
    decoder = Decoder(target_vocab, embedding_dim, hidden_dim, decoder_model)

    # 입력 텐서 생성
    sample_source = torch.randint(0, source_vocab.vocab_size, (batch_size, 10))  # 예시 시퀀스 길이 10
    sample_target = torch.randint(0, target_vocab.vocab_size, (batch_size, 10))  # 예시 시퀀스 길이 10

    # encoder의 출력 shape 확인
    encoder_output = encoder(sample_source)
    print("Encoder output shape:", encoder_output.shape)

    # decoder의 출력 shape 확인
    decoder_output = decoder(sample_target, encoder_output)
    print("Decoder output shape:", decoder_output.shape)

    model = Seq2Seq(encoder = encoder, 
                    decoder = decoder,)
    
    model.train()
    loss = 0
    loss_history = []
    
    criterion = criterion()
    
    optimizer = optimizer(model.parameters(), lr = learning_rate)
    for epoch in range(1, num_epochs + 1):
        epoch_loss = 0
        for step_idx, (source_batch, target_batch) in enumerate(train):
            optimizer.zero_grad()
            
            pred_batch = model(source_batch, target_batch)
            batch_size, seq_length = target_batch.size()
            
            loss = criterion(pred_batch.view(batch_size * seq_length, -1), target_batch.view(-1))

            loss.backward() 
            optimizer.step()
            
            epoch_loss += loss 

            if step_idx % 100 == 0:
                print(f'[Epoch {epoch}/{num_epochs}] step {step_idx}: loss - {loss}')

        avg_loss = epoch_loss.item() / len(train)
        loss_history.append(avg_loss)
    plt.plot(loss_history)
    plt.show()
            