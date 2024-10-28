import torch 
from torch.utils.data import DataLoader, random_split 

from collections import defaultdict
#from debug_shell import debug_shell 
"""
1. 토큰별 정확도
2. 입출력에 직접 입력해 결과확인

"""

class Vocabulary:
    PAD = '[PAD]'
    SOS = '[SOS]'
    EOS = '[EOS]'
    OOV = '[OOV]'
    SPECIAL_TOKENS = [PAD, SOS, EOS, OOV] 
    PAD_IDX = 0
    SOS_IDX = 1 
    EOS_IDX = 2 
    OOV_IDX = 3

    def __init__(self, word_count, coverage = 0.999):
        word_freq_list = []
        total = 0

        for word, freq in word_count.items():
            word_freq_list.append((word, freq))
            total += freq

        word_freq_list = sorted(word_freq_list, key = lambda x : x[1], reverse = True)

        word2idx = {}
        idx2word = {}
        s = 0

        for idx, (word, freq) in enumerate([(e, 0)for e in Vocabulary.SPECIAL_TOKENS] + word_freq_list):
            s += freq
            if s > coverage * total:
                break
            word2idx[word] = idx
            idx2word[word] = word

        self.word2idx = word2idx
        self.idx2word = idx2word
        self.vocab_size = len(word2idx)

    def word_2_idx(self, word):
        if word in self.word2idx:
            return self.word2idx[word]
        return Vocabulary.OOV_IDX
    

def parse_file(file_path, train_volid_test_ratio = (0.8, 0.1, 0.1),
               batch_size = 32):
    f = open(file_path, "r", encoding = "utf-8")
    data = []

    source_word_count = defaultdict(int)
    target_word_count = defaultdict(int)

    for line in f.readlines():
        line = line.strip()
        lst = line.split('\t')
        
        if len(lst) == 3:
            source, target, etc = lst
        else:
            source, target = lst 

        source = source.split()
        for source_token in source:
            source_word_count[source_token] += 1

        target = target.split()
        for target_token in target:
            target_word_count[target_token] += 1

        data.append((source, target))

    source_vocab = Vocabulary(source_word_count)
    target_vocab = Vocabulary(target_word_count)

    for idx, (source, target) in enumerate(data):
        data[idx] = (
            list(map(source_vocab.word_2_idx, source)),
            list(map(target_vocab.word_2_idx, target))
        )
        
    lengths = [int(len(data) * ratio) for ratio in train_volid_test_ratio]
    lengths[-1] = len(data) - sum(lengths[:-1])
    datasets = random_split(data, lengths)

    dataloaders = [
        DataLoader(dataset,
                   batch_size = batch_size,
                   shuffle = True,
                   collate_fn= lambda x:preprocess(x, source_vocab, target_vocab)) for dataset in datasets]
    
    return dataloaders, source_vocab, target_vocab


def preprocess(batches, input_vocab, answers_vocab):
    inputs = [a[0] for a in batches]
    answers = [a[1] for a in batches]

    input_seqs = []
    answer_seqs = []

    for input_seq in inputs:
        input_seqs.append(input_seq + [input_vocab.EOS_IDX])

    for answer_seq in answers:
        answer_seqs.append(answer_seq + [answers_vocab.EOS_IDX])
    
    input_max_length = max([len(s) for s in input_seqs])
    answer_max_length = max([len(s) for s in answer_seqs])

    for idx, seq in enumerate(input_seqs):
        seq = seq + [input_vocab.PAD_IDX] * (input_max_length - len(seq))
        assert len(seq) == input_max_length, f'Expected to have {input_max_length}, now {len(seq)}'
        input_seqs[idx] = seq

    for idx, seq in enumerate(answer_seqs):
        seq = seq + [answers_vocab.PAD_IDX] *(answer_max_length - len(seq))
        assert len(seq) == answer_max_length, f"Expected to have {answer_max_length}, now {len(seq)}"
        answer_seqs[idx] = seq

    return torch.tensor(input_seqs), torch.tensor(answer_seqs)





if __name__ == '__main__':
    from code import interact 
    batch_size = 32 
    (train, valid, test), source_vocab, target_vocab = parse_file('kor.txt', batch_size = batch_size)
    
    for source_batch, target_batch in train:
        assert source_batch.shape[0] == batch_size
        print(source_batch) 
        
        assert target_batch.shape[0] == batch_size 
        print(target_batch)
