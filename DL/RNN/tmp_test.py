train_dataset, valid_dataset, test_dataset, alphabets, max_length, languages  = generate_dataset()

rnn = RecurrentNeuralNetwork(128, alphabets_99, all_languages)
train_loss_history, valid_loss_history = rnn.train_model(train_dataset, valid_dataset)

plot_loss_history(train_loss_history, valid_loss_history, train_loss_history, valid_loss_history)
