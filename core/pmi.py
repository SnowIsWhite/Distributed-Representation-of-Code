import json
import ast
import Queue
import operator
from utility import read_unigram, read_bigram, tree_to_string

class Tree: 
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        self.number = 0
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def __num__(self):
        return self.number
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)    

def get_unigram_cnt(bi_tree, unigram):
    uni_cnt = []
    # bi_tree -> tree
    bi_tree = ast.literal_eval(bi_tree)
    
    # get all unigrams
    q = Queue.Queue()
    q.put(0)
    while not q.empty():
        i = q.get_nowait()
        if 'children' not in bi_tree[i]: continue
        for child in bi_tree[i]['children']: q.put(child)
        tree = Tree(name=bi_tree[i]['type'])
        for child in bi_tree[i]['children']:
            tree.add_child(Tree(name=bi_tree[child]['type']))
        uni_cnt.append(unigram[tree_to_string(tree)])        
    return uni_cnt

def calculate_score(bi_cnt, uni_cnt):
    # return score
    prod = 1
    for c in uni_cnt:
        prod = prod * c
    score = bi_cnt/(prod*1.)
    return score

def print_statistics(bigram_score):
    print("\n\n========STAT========\n")
    # avg, min, max, q1, q2, q3
    sorted_score = sorted(bigram_score.items(), key=operator.itemgetter(1), reverse=True)
    total = len(sorted_score)
    total_score = 0
    for i, t in sorted_score:
        total_score += t
    print("Average: {}\n".format(str(total_score/(len(sorted_score)*1.))))
    q = [0,0,0]
    for i, t in sorted_score:
        if i >= int(total*0.25) and q[0]==0:
            print("Q1: {}".format(str(t)))
            q[0] = 1
        elif i >= int(total*0.5) and q[1]==0:
            print("Q2: {}".format(str(t)))
            q[1] = 1
        elif i >= int(total*0.75) and q[2]==0:
            print("Q3: {}".format(str(t)))
            break
    print("Max: {}".format(str(sorted_score[0][1])))
    print("Min: {}".format(str(sorted_score[-1][1])))
    print("===========================\n\n")
    return

if __name__ == "__main__":
    bigram = read_bigram()
    unigram = read_unigram()
    bigram_score = {}
    # calculate score
    total_bigram_cnt = len(bigram)
    print("Total bigrmas: {}".format(str(total_bigram_cnt)))
    for idx, bi_tree in enumerate(bigram):
        if idx % 10000 == 0:
            print("{}th bigram: {}% done".format(str(idx), str(idx/(total_bigram_cnt*1.))))
        uni_cnt = get_unigram_cnt(bi_tree, unigram)
        bigram_score[bi_tree] = calculate_score(bigram[bi_tree], uni_cnt)
    
    # statistics
    print_statistics(bigram_score)

    # write file
    with open('./bigram_score.json', 'w') as jsonfile:
        tmp = json.dumps(bigram_score)
        jsonfile.write(tmp)    
