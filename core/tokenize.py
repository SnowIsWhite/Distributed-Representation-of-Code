# tokenize ast according to tree dictionary
# return list of list
# e.g. [[token, token, token], [token, token, token]]
import json
import ast
import Queue
from utility import read_unigram, read_bigram, tree_to_string

result_path = './tokenized_data.json'
data_path = './python100k_train_function.json'
UNSEEN = 'UNK'

class Tree:
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        self.number = 0
    def __repr__(self):
        return self.name
    def __num__(self):
        return self.number
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)
    
def write_data(result):
    with open(result_path, 'w') as f:
        tmp = json.dumps(result)
        f.write(tmp)

def tokenize_unigram(unigram, target):
    global UNSEEN
    sentence = []
    q = Queue.Queue()
    q.put(0)
    while not q.empty():
        i = q.get_nowait()
        if 'children' not in target[i]: continue
        for child in target[i]['children']: q.put(child)
        root = Tree(name=target[i]['type'])
        for child in target[i]['children']:
            root.add_child(Tree(name=target[child]['type']))
        uni = tree_to_string(root)
        if uni in unigram:
            sentence.append(uni)
        else:
            sentence.append(UNSEEN)
    return sentence

def tokenize_bigram(bigram, unigram, target):
    return

if __name__ == "__main__":
    test_num = 10000
    selector = 0
    # 0: unigram, 1: bigram
    bigram = read_bigram()
    unigram = read_unigram()
    
    result = []
    with open(data_path, 'r') as f:
        for idx, line in enumerate(f.readlines()):
            if idx > test_num: break
            if idx % 1000 == 0: print("test num : {}".format(str(idx)))
            line = ast.literal_eval(line)
            if selector == 0:
                res = tokenize_unigram(unigram, line)
            else:
                res = tokenize_bigram(bigram, unigram, line)
            result.append(res)
    write_data(result)
            
