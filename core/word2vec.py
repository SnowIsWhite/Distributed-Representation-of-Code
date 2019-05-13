import os
import json
import ast
import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

selector = 0
trees_path = './tokenized_data.json'
trees_path_bigram = './tokenized_data_bigram.json'
wv_path = './wv_model/vectors.kv'
# list of list of tokens

if selector == 1: trees_path = trees_path_bigram
with open(trees_path, 'r') as f:
    lines = f.readline()
sentences = ast.literal_eval(lines)
model = gensim.models.Word2Vec(sentences=sentences, window=2, workers=4, sg=1, iter=100)
model.wv.save(wv_path)
