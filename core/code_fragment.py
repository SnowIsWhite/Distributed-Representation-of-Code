import json
import Queue
import itertools
import operator
import ast as ast_lib
from copy import deepcopy

#train_data_dir = '/Users/jaeickbae/Documents/research/program_synthesis/python150/py150/python100k_train.json'
test_data = './python100k_train_function.json'
# loop for all data
# break down into fragments
# stringify
# save in dictionary(1 depth, 2 depth, ...)

class CodeNgram:
    def __init__(self, depth):
        self.depth = depth
        self.forest = {}
    def __repr__(self):
        return self.forest
    def add_tree(self, tree):
        if tree not in self.forest:
            self.forest[tree] = 1
        else:
            self.forest[tree] += 1
    def delete_rare_tree(self, thresh):
        self.forest = {key:val for key, val in self.forest.items() if val > thresh}

class Tree:
    "Generic tree node."
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
    def change_number(self, num):
        self.number = num

def __get_appended_tree(curr, tree, permutation, ast, to_traverse):
    for i, b in enumerate(permutation):
        if b:
            target_child_idx = to_traverse[i]
            on_ast_child_node_idx = ast[curr]['children'][target_child_idx]
            on_ast_grandchild_node_idx_list = ast[on_ast_child_node_idx]['children']
            for grandchild_idx in on_ast_grandchild_node_idx_list:
                node = Tree(name=ast[grandchild_idx]['type'])
                tree.children[target_child_idx].add_child(node)
    return tree

def tree_to_string(tree):
    stack = []
    stack.append(tree)
    cnt = 0
    while len(stack)!=0:
        node = stack.pop()
        node.number = cnt
        cnt += 1
        for child in reversed(node.children):
            stack.append(child)

    string_tree = []
    stack = []
    stack.append(tree)
    while len(stack)!=0:
        node = stack.pop()
        element = {}
        element['type'] = node.__repr__()
        if len(node.children)!=0:
            element['children'] = []
            for child in node.children:
                element['children'].append(child.__num__())
            for child in reversed(node.children):
                stack.append(child)
        string_tree.append(element)
    string_tree = json.dumps(string_tree)
    return string_tree

def break_into_fragments(ast, depth, ngram_dic=None):
    fragments = []
    q = Queue.Queue()
    q.put(0)
    while not q.empty():
        i = q.get_nowait()
        if 'children' not in ast[i]: continue
        for child in ast[i]['children']: q.put(child)
        if depth == 1:
            tree = Tree(name=ast[i]['type'])
            for child in ast[i]['children']:
                tree.add_child(Tree(name=ast[child]['type']))
            # stringify the tree and add to fragments
            fragments.append(tree_to_string(tree))
        elif depth == 2:
            tree = Tree(name=ast[i]['type'])
            for child in ast[i]['children']:
                tree.add_child(Tree(name=ast[child]['type']))
            if tree_to_string(tree) not in ngram_dic:
                continue
            to_traverse = []
            for idx, child in enumerate(ast[i]['children']):
                if 'children' in ast[child]:
                    # check the child tree exists in unigram
                    tree3 = Tree(name=ast[child]['type'])
                    for grand in ast[child]['children']:
                        tree3.add_child(Tree(name=ast[grand]['type']))
                    if tree_to_string(tree3) not in ngram_dic:
                        continue
                    to_traverse.append(idx)
            if len(to_traverse) == 0: continue
            l = [True, False]
            permute = list(itertools.product(l,repeat=len(to_traverse)))
            for p in permute:
                if not any(p): continue
                temp_tree = deepcopy(tree)
                tree2 = __get_appended_tree(i, tree, list(p), ast, to_traverse)
                tree = deepcopy(temp_tree)
                # stringify tree
                fragments.append(tree_to_string(tree2))
    return fragments

def show_ngram_stat(ngram_dic):
    print("\n==== STAT 2 ====\n")
    # sort
    sorted_dic = sorted(ngram_dic.items(), key=operator.itemgetter(1), reverse=True)
    name_erased = [(idx+1, tup[1]) for idx, tup in enumerate(sorted_dic)]
    # print
    tot = 0
    for i, t in name_erased:
        tot += t
    cnt = 0
    q = [0,0,0]
    for i, t in name_erased:
        if cnt > int(tot*0.25) and q[0]==0:
            print("Q1: {}".format(str(t)))
            q[0] = 1
        elif cnt > int(tot*0.5) and q[1]==0:
            print("Q2: {}".format(str(t)))
            q[1] = 1
        elif cnt > int(tot*0.75) and q[2]==0:
            print("Q3: {}".format(str(t)))
            q[2] = 1
        elif cnt > int(tot*0.97):
            print("97%: {}".format(str(t)))
            thresh=t
            break
        cnt += t
    print("Max: {}".format(str(sorted_dic[0][1])))
    print("Min: {}\n".format(str(sorted_dic[-1][1])))
    print("=====================\n\n")
    return thresh

def check_ratio(ngram_dic):
    overlaps = 0
    entire = 0
    for key in ngram_dic:
        if ngram_dic[key] != 1:
            overlaps += ngram_dic[key]
        entire += ngram_dic[key]

    print("\n==== STAT 1 ====\n")
    print("whole data: {}".format(str(entire)))
    print("Ratio of overlapping data: {}, {}%\n".format(str(overlaps), str(overlaps/(entire*1.)*100)))
    print("==================\n\n")

if __name__ == "__main__":
    test_num = 1000
    one_gram = CodeNgram(depth=1)
    with open(test_data, 'r') as file:
        print("Start on One Gram...")
        raw_data = file.readlines()
        for idx, line in enumerate(raw_data):
            if idx > test_num:
                break
            if idx % 10000 == 0:
                print("{}th function".format(str(idx)))
            ast = ast_lib.literal_eval(line)
            fragments = break_into_fragments(ast, depth=1, ngram_dic={})
            for fr in fragments:
                one_gram.add_tree(fr)
    check_ratio(one_gram.__repr__())
    one_gram.delete_rare_tree(thresh=1)
    thresh = show_ngram_stat(one_gram.__repr__())
    one_gram.delete_rare_tree(thresh=thresh)
    # write dictionary
    with open('./one_gram.json', 'w') as jsonfile:
        temp = json.dumps(one_gram.__repr__())
        jsonfile.write(temp)

    # bigram
    print("Start bigram...")
    bigram = CodeNgram(depth=2)
    for idx, line in enumerate(raw_data):
        if idx > test_num:
            break
        if idx % 10000 == 0:
            print("{}th function".format(str(idx)))
        ast = ast_lib.literal_eval(line)
        fragments = break_into_fragments(ast, depth=2, ngram_dic=one_gram.__repr__())
        for fr in fragments:
            bigram.add_tree(fr)
    check_ratio(bigram.__repr__())
    bigram.delete_rare_tree(thresh=1)
    thresh = show_ngram_stat(bigram.__repr__())
    bigram.delete_rare_tree(thresh=thresh)
    with open('./bigram.json', 'w') as jsonfile:
        temp = json.dumps(bigram.__repr__())
        jsonfile.write(temp)

