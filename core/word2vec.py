import os
import json
import ast
import gensim, logging

from gensim.models.callbacks import CallbackAny2Vec
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class callback(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 0
        self.loss_history = []
        self.prev_loss = 0
    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        print("epoch {} loss : {}".format(str(self.epoch), str(loss)))
        self.epoch += 1
        self.loss_history.append(loss - self.prev_loss)
        self.prev_loss = loss
    def __loss__(self):
        return self.loss_history

selector = 1
trees_path = './tokenized_data.json'
trees_path_bigram = './tokenized_data_bigram.json'
wv_path = './wv_model/vectors.kv'
# list of list of tokens

if selector == 1: trees_path = trees_path_bigram
with open(trees_path, 'r') as f:
    lines = f.readline()
sentences = ast.literal_eval(lines)
c = callback()
model = gensim.models.Word2Vec(sentences=sentences, window=3, workers=4, sg=1, iter=1000, compute_loss=True, callbacks=[c])
model.wv.save(wv_path)

with open('./misc/train_loss.txt', 'w') as f:
    for h in c.__loss__():
        f.write(str(h))
        f.write('\n')
