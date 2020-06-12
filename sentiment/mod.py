import torch.nn as nn
import torch
import torchtext.data as data
import torch.nn.functional as F
import numpy as np

class RNN(nn.Module):

    def __init__(self, vocab_size, embedding_dim, padding_idx, hidden_dim, num_layers, bidirectional, dropout, output_dim):
        super(RNN,self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=padding_idx)
        self.rnn = nn.LSTM(embedding_dim, hidden_dim, num_layers=num_layers, bidirectional=bidirectional, dropout=dropout)
        self.dropout = nn.Dropout(dropout)
        self.decoder = nn.Linear(hidden_dim*2, output_dim)
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.output_dim = output_dim

    def forward(self, text, hidden):
        #embedded=[sentence_len,batch_size,embedding_dim]
        embedded = self.dropout(self.embedding(text))
        #output=[sentence_len,batch_size,hidden_dim*num_directional]
        #hidden=[num_layers*num_directional,batch_size,hidden_dim]
        #cell=[num_layers*num_directional,batch_size,hidden_dim]
        output, (hidden, cell) = self.rnn(embedded, hidden)
        decoded = self.decoder(self.dropout(torch.cat((hidden[-2,:,:],hidden[-1,:,:]),dim=1)))
        return decoded, (hidden, cell)

    def init_hidden(self, batch_size, requires_grad=True):
        weight = next(self.parameters())
        return (
            weight.new_zeros((self.num_layers*2, batch_size, hidden_dim),requires_grad=requires_grad),
            weight.new_zeros((self.num_layers*2, batch_size, hidden_dim),requires_grad=requires_grad)
        )

vocab_size = 8167
embedding_dim = 100
padding_idx = 1
hidden_dim = 128
num_layers = 2
bidirectional = True
dropout = 0.5
output_dim = 2

# model = RNN(vocab_size, embedding_dim, padding_idx, hidden_dim, num_layers, bidirectional, dropout, output_dim)

# 情感分析
def predict_sentiment(sentence):

    model = RNN(vocab_size, embedding_dim, padding_idx, hidden_dim, num_layers, bidirectional, dropout, output_dim)
    stoi = np.load('stoi.npy').item()
    device = torch.device('cpu')
    #     model = TheModelClass(*args, **kwargs)
    model.load_state_dict(torch.load('qingganfenxi-model.pt', map_location=device))
    hidden = model.init_hidden(1)
    tokenized = [tok for tok in sentence]
    indexed = [stoi[t] for t in tokenized]
    tensor = torch.LongTensor(indexed).to(device)
    tensor = tensor.unsqueeze(1)
    output, hidden = model(tensor, hidden)
    output = output[0]

    prediction = F.softmax(output,dim=0)
    max_ = [i for i,j in enumerate(prediction) if j == max(prediction)][0]
    if max_ == 0:
        return 1
    if max_ == 1:
        return 0