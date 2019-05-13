# tokenize ast according to tree dictionary
# return list of list
# e.g. [[token, token, token], [token, token, token]]
import json
import ast
import Queue
from utility import read_unigram, read_bigram, tree_to_string
from utility import read_bigram_score

result_path = './tokenized_data.json'
result_path_bigram = './tokenized_data_bigram.json'
data_path = './python100k_train_function.json'
UNSEEN = 'UNK'
THRESH = 0.27
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
    
def write_data(result, selector):
    if selector == 1: result_path = result_path_bigram
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

def tokenize_bigram(bigram, bigram_score, unigram, target):
    global UNSEEN
    global THRESH
    sentence = []
    vis = [0] * len(target)
    q = Queue.Queue()
    q.put(0)
    while not q.empty():
        i = q.get_nowait()
        if vis[i] == 1: continue
        if 'children' not in target[i]:
            vis[i] = 1    
            continue
        for child in target[i]['children']: q.put(child)
        # search bigram
        tree = Tree(name=target[i]['type'])
        for child in target[i]['children']:
            tree.add_child(Tree(name=target[child]['type']))
        if tree_to_string(tree) not in unigram:
            sentence.append(UNSEEN)
            vis[i] = 1
            continue
        # depth 2 tree
        to_traverse = []
        for child in target[i]['children']:
            if 'children' in target[child]:
                subtree = Tree(name=target[child]['type'])
                for grand in target[child]['children']:
                    subtree.add_child(Tree(name=target[grand]['type']))
                if tree_to_string(subtree) not in unigram:
                    continue
                to_traverse.append(child)
        # depth 2 tree doesn't exist
        if len(to_travesre) == 0:
            # color unigram
            vis[i] = 1
            sentence.append(tree)
            continue
        # get all bigrams
        num_nodes = len(to_traverse)
        while num_nodes > 0:
            tmp_tree = deepcopy(tree)
            bi_tree = __get_appended_tree()
            str_bi_tree = tree_to_string(bi_tree)
            if str_bi_tree in bigram_score:
                if bigram_score[str_bi_tree] >= THRESH:
                     
        
    # if there exists color it
    # search unigram
    return

if __name__ == "__main__":
    test_num = 10000
    selector = 0
    # 0: unigram, 1: bigram
    bigram = read_bigram()
    unigram = read_unigram()
    bigram_score = read_bigram_score()  
    result = []
    with open(data_path, 'r') as f:
        for idx, line in enumerate(f.readlines()):
            if idx > test_num: break
            if idx % 1000 == 0: print("test num : {}".format(str(idx)))
            line = ast.literal_eval(line)
            if selector == 0:
                res = tokenize_unigram(unigram, line)
            else:
                res = tokenize_bigram(bigram, bigram_score, unigram, line)
            result.append(res)
    write_data(result, selector)
            
