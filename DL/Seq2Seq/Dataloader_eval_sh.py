from torch.utils.data import DataLoader, random_split
import torch
import torch.nn as nn
import random
import os
from sh_Vocabulary import collate_fn_language, Vocabulary

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

#trainmodel
class Train_model(nn.Module):
    def __init__(self, model, device, criterion, optimizer, max_target_len = 100, save_dir = "save_models"):
        super(Train_model, self).__init__()

        self.model = model.to(device)
        self.device = device
        self.criterion = criterion
        self.optimizer = optimizer
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok = True)
        self.max_target_len = max_target_len

        self.train_lossese = []
        self.val_losses = []
        self.val_metrics = []
        self.best_val_loss = float("inf")
        self.best_model_state = None

    def train(self, train_loader, valid_loader = None, num_epochs = 10, print_every = 1, evaluate_every = 1, evaluate_metric = "accuracy"):

        value_counter = 0
        for epoch in range(1, num_epochs + 1):
            self.model.train()
            epoch_train_loss = 0

            for batch_idx, (source, target) in enumerate(train_loader):
                source = source.to(self.device)
                target = target.to(self.device)

                self.optimizer.zero_grad()
                output = self.model(source, target)

                output_dim = output.shape[-1]
                output = output.reshape(-1, output_dim)
                target = target.reshape(-1)

#evaluate

