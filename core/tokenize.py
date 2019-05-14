# tokenize ast according to tree dictionary
# return list of list
# e.g. [[token, token, token], [token, token, token]]
import json
import ast
import Queue
import itertools
from copy import deepcopy
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
    stack = []
    stack.append(0)
    while len(stack)!=0:
        i = stack.pop()
        if 'children' not in target[i]:
            vis[i] = 1    
            continue
        for child in reversed(target[i]['children']): stack.append(child)
        if vis[i] == 1: continue
        # search bigram
        tree = Tree(name=target[i]['type'])
        for child in target[i]['children']:
            tree.add_child(Tree(name=target[child]['type']))
        str_tree = tree_to_string(tree)
        if str_tree not in unigram:
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
        if len(to_traverse) == 0:
            # color unigram
            vis[i] = 1
            sentence.append(str_tree)
            continue

        # get all bigrams
        num_nodes = len(to_traverse)
        max_score = 0
        while num_nodes > 0:
            # get appended tree, changed vis index
            if num_nodes == len(to_traverse):
                permute = [tuple(to_traverse)]
            else:
                permute = itertools.permutations(to_traverse, num_nodes)
            for tup in permute:
                tmp_vis = [v for v in vis]
                tmp_tree = deepcopy(tree)
                tmp_vis[i] = 1
                for child in tup:
                    for idx, c in enumerate(target[i]['children']):
                        if c == child:
                            tmp_vis[c] = 1
                            for grand in target[child]['children']:
                                tmp_tree.children[idx].add_child(Tree(name=target[grand][
'type']))
                str_bi_tree = tree_to_string(tmp_tree)
                if str_bi_tree not in bigram: continue
                if bigram_score[str_bi_tree] > max_score:
                    max_score = bigram_score[str_bi_tree]
                    final_vis = [v for v in tmp_vis]
                    tmp_str_bi_tree = str_bi_tree
            num_nodes -= 1
        # final check
        if max_score > THRESH:
            vis = [v for v in final_vis]
            sentence.append(tmp_str_bi_tree)
        else:
            vis[i] = 1
            sentence.append(str_tree)                   
    return sentence

if __name__ == "__main__":
    test_num = 1000
    selector = 1
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
            
