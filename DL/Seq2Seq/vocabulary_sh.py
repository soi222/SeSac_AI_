from torch.utils.data import DataLoader, random_split
import torch
import torch.nn as nn
import random


class Vocabulary:
    PAD = "[PAD]"
    SOS = "[SOS]"
    EOS = "[EOS]"
    OOV = "[OOV]"
    pad_idx = 0
    sos_idx = 1
    eos_idx = 2
    oov_idx = 3
    SPECIAL_TOKENS = [PAD, SOS, EOS, OOV]

    def __init__(self, word_threshold = 0):
        self.word2index = {}
        self.index2word = {}
        self.word_count = {}
        self.n_words = 0 #including PAD, SOS, EOS, OOV token
        self.threshold = word_threshold

        self.pad_idx = Vocabulary.pad_idx
        self.sos_idx = Vocabulary.sos_idx
        self.eos_idx = Vocabulary.eos_idx
        self.oov_idx = Vocabulary.oov_idx

        self.add_the_word(Vocabulary.PAD)
        self.add_the_word(Vocabulary.SOS)
        self.add_the_word(Vocabulary.EOS)
        self.add_the_word(Vocabulary.OOV)

    def add_sentence(self, sentence):
        for word in sentence:
            self.add_the_word(word)


    def add_the_word(self, new_word):
        if new_word not in self.word2index: 
            self.word2index[new_word] = self.n_words 
            self.word_count[new_word] = 1
            self.index2word[self.n_words] = new_word
            self.n_words += 1
        else:
            self.word_count[new_word] += 1

    def word_to_idx(self, word):
        return self.word2index.get(word, self.oov_idx) 
        #get(가져올 key.value, 해당 key가 없는 경우 가져올 값)


def idx_to_word(self, idx):
    return self.index2word.get(idx, self.oov_idx)

def idx_to_one_hot(batch, vocab_dim):
    assert batch.dim() == 2, f"Input batch should have 2 dimensions, but got {batch.dim()}.."
    batch_size, seq_length = batch_size()

    one_hot = torch.zeros(batch_size, seq_length, vocab_dim).to(batch.device)
    one_hot.scatter_(2, batch.unsqueeze(2), 1) #[batch_size, seq_length, vocab_size]

    assert one_hot.size() == (batch_size, seq_length, vocab_dim), f"Output should have shape {(batch_size, seq_length, vocab_dim)} but got {one_hot.size()}"

    return one_hot

def generate_target_sequence(input_seq, length, lookback = 3, mod = 10):
    result = []

    for idx in range(length):
        if idx < lookback: #special tokens 
            result.append(sum(input_seq[-lookback + idx] + result[:idx]) % mod)

        else:
            result.append(sum(result[-lookback:]) % mod)

    return result

def create_interger_sequence_dataset(num_samples = 1000, max_input_len = 10, max_target_len = 15, vocab_size = 20, batch_size = 32, train_valid_test = (0.8, 0.1, 0.1)):
    vocab = Vocabulary()
    no_speical_token = len(Vocabulary.SPECIAL_TOKENS)
    for i in range(no_speical_token, vocab_size):
        vocab.add_the_word(str(i))
    
    data = []

    for _ in range(num_samples):
        input_len = random.randint(3, max_input_len)

        input_seq = [random.randint(no_speical_token, vocab_size - 1)for _ in range(input_len)]
        target_seq = input_seq
        #target_seq = generate_target_sequence(input_seq, max_target_len)

        data.append((input_seq, target_seq))

    lengths = [int(num_samples * ratio) for ratio in train_valid_test]
    lengths[-1] = num_samples - sum(lengths[:-1])

    datasets = random_split(data, lengths)
    dataloaders = [DataLoader(dataset, batch_size = batch_size, shuffle = True, collate_fn = collate_func) for dataset in datasets]

    return dataloaders, vocab


def collate_func(batch):
    input_seqs = [batch_babe[0] for batch_babe in batch]
    target_seqs = [batch_babe[1] for batch_babe in batch]

    input_seqs = [seq + [Vocabulary.eos_idx]for seq in input_seqs]
    target_seqs = [[Vocabulary.sos_idx] + seq + [Vocabulary.eos_idx]for seq in target_seqs]

    input_max_len = max([len(seq) for seq in input_seqs])
    target_max_len = max([len(seq) for seq in target_seqs])

    input_padd = []
    for seq in input_seqs:
        seq = seq + [Vocabulary.pad_idx] * (input_max_len - len(seq))
        input_padd.append(seq)

    target_padd = []
    for seq in target_seqs:
        seq = seq + [Vocabulary.pad_idx] * (target_max_len - len(seq))
        target_padd.append(target_padd)

    input_padd = torch.tensor(input_padd, dtype=torch.long) #
    target_padd = torch.tensor(target_padd, dtype=torch.long)

    return input_padd, target_padd


#idx + paded
def collate_fn_language(batch, source_vocab, target_vocab):
    input_seqs = [item[0] for item in batch]
    target_seqs = [item[1] for item in batch]

    input_seq_indices = []
    for seq in input_seqs:
        seq_indices = [source_vocab.word_to_idx(word) for word in seq] + [source_vocab.eos_idx]
        input_seq_indices.append(seq_indices)

    target_seq_indices = []
    for seq in target_seqs:
        seq_indices = [target_vocab.sos_idx] + [target_vocab.word_to_idx(word) for word in seq] + [target_vocab.eos_idx]
        target_seq_indices.append(seq_indices)


    input_max_len = max([len(seq) for seq in input_seq_indices])
    target_max_len = max([len(seq) for seq in target_seq_indices])

    input_padd = []
    for seq in input_seq_indices:
        seq = seq + [source_vocab.pad_idx] * (input_max_len - len(seq))
        input_padd.append(seq)

    target_padd = []
    for seq in target_seq_indices:
        seq = seq + [source_vocab.pad_idx] * (target_max_len -len(seq))
        target_padd.append(seq)

    input_padd = torch.tensor(input_padd, dtype= torch.long)
    target_padd = torch.tensor(target_padd, dtype= torch.long)

    return input_padd, target_padd


def create_lang_pair(data_file, batch_size = 32, train_valid_test = (0.8,0.1,0.3)):
    source_vocab = Vocabulary()
    target_vocab = Vocabulary()

    text = open(data_file, "r", encoding="utf-8").read()
    data = []
    num_samples = 0
    for line in text.split("\n"):
        line = line.strip()

        try:
            source, target, _ = line.split("\t")
        except ValueError:
            try:
                source, target = line.split("\t")
            except ValueError:
                continue

        source = source.strip().split()
        target = target.strip().split()
        source_vocab.add_sentence(source)
        target_vocab.add_sentence(target)

        data.append((source, target))
        num_samples += 1

    lengths = [int(num_samples * ratio) for ratio in train_valid_test]
    lengths[-1] = num_samples - sum(lengths[:-1])

    datasets = random_split(data, lengths)
    dataloaders = [DataLoader(dataset, batch_size =  batch_size, shuffle= True, collate_fn= lambda x: collate_fn_language(x, source_vocab, target_vocab)) for dataset in datasets]

    return dataloaders, source_vocab, target_vocab


if __name__ == "__main__":
    (train, valid, test), source_vocab, target_vocab = create_lang_pair("eng-fra.txt")

    for x, y in train:
        print(x[0])
        print(y[0])
        break

    