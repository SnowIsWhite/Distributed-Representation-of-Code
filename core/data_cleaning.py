# erase bigrams that overlaps with a bigger bigram which includes the bigram

import json
import ast
import Queue
import itertools
from copy import deepcopy

unigram_file_path = './one_gram.json'
bigram_file_path = './bigram.json'
train_file_path = './python100k_train_function.json'
observation_path = './data_observation/ob{}'

tot_delete = 0
doc_cnt = 0

class Tree:
    def __init__(self, name='root', value=None, children=None):
        self.name = name
        self.children = []
        self.number = 0
        self.value = value
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def __num__(self):
        return self.number
    def __value__(self):
        return self.value
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)
    def change_number(self, num):
        self.number = num

def read_dictionary():
    with open(unigram_file_path, 'r') as jsonfile:
        line = jsonfile.readline()
        unigram = ast.literal_eval(line)
    with open(bigram_file_path, 'r') as jsonfile:
        line = jsonfile.readline()
        bigram = ast.literal_eval(line)
    return unigram, bigram

def replace_dictionary(bigram):
    with open(bigram_file_path, 'w') as jsonfile:
        temp = json.dumps(bigram)
        jsonfile.write(temp)
    return

def tree_to_string(root):
    stack = []
    stack.append(root)
    cnt = 0
    while len(stack)!=0:
        node = stack.pop()
        node.number = cnt
        cnt += 1
        for child in reversed(node.children):
            stack.append(child)

    string_tree = []
    stack = []
    stack.append(root)
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

def write_observation(t1, v1, t2, v2):
    global doc_cnt
    with open(observation_path.format(str(doc_cnt)), 'w') as f:
        f.write(t1)
        f.write("\n\n==================\n\n")
        f.write(t2)
        f.write("\n\n")
        f.write(str(v1))
        f.write("\n")
        f.write(str(v2))
    doc_cnt += 1
    return

def delete_from_dic(bigram, curr, num_nodes, to_traverse, tmp_tree, ast_tree):
    global tot_delete
    if num_nodes == len(to_traverse):
        permute = [tuple(to_traverse)]
    else:
        permute = itertools.permutations(to_traverse, num_nodes)
    for tup in permute:
        tmp_tree2 = deepcopy(tmp_tree)
        for child in tup:
            for idx, c in enumerate(ast_tree[curr]['children']):
                if c == child:
                    for grand in ast_tree[child]['children']:
                        tmp_tree2.children[idx].add_child(Tree(name=ast_tree[grand]['type']))
        str_tree2 = tree_to_string(tmp_tree2)
        if str_tree2 not in bigram:
            return
        val_of_tree = bigram[str_tree2]
        num_nodes -= 1
        permute2 = itertools.permutations(to_traverse, num_nodes)
        num_nodes += 1
        for tup2 in permute2:
            tmp_tree3 = deepcopy(tmp_tree)
            for child in tup2:
                for idx, c in enumerate(ast_tree[curr]['children']):
                    if c == child:
                        for grand in ast_tree[child]['children']:
                            tmp_tree3.children[idx].add_child(Tree(name=ast_tree[grand]['type']))
            str_tree3 = tree_to_string(tmp_tree3)
            if str_tree3 not in bigram:
                continue
            val_of_tree2 = bigram[str_tree3]
            if val_of_tree == val_of_tree2:
                del bigram[str_tree3]
                tot_delete += 1
                if tot_delete % 10 == 0:
                    print("tot_delete: {}".format(str(tot_delete)))
            else:
                write_observation(str_tree2, val_of_tree, str_tree3, val_of_tree2)
    return

def cleaning(unigram, bigram, ast_tree):
    # delete some keys in bigram dictionary
    q = Queue.Queue()
    q.put(0)
    while not q.empty():
        i = q.get_nowait()
        if 'children' not in ast_tree[i]: continue
        for child in ast_tree[i]['children']: q.put(child)
        root = Tree(name=ast_tree[i]['type'])
        for child in ast_tree[i]['children']:
            root.add_child(Tree(name=ast_tree[child]['type']))
        if tree_to_string(root) not in unigram:
            continue
        to_traverse = []
        for idx, child in enumerate(ast_tree[i]['children']):
            if 'children' in ast_tree[child]:
                # check the child tree exists in unigram
                tmp_tree = Tree(name=ast_tree[child]['type'])
                for grand in ast_tree[child]['children']:
                    tmp_tree.add_child(Tree(name=ast_tree[grand]['type']))
                if tree_to_string(tmp_tree) not in unigram:
                    continue
                to_traverse.append(child)
        num_nodes = len(to_traverse)
        while num_nodes > 1:
        #    print("Num nodes : {}".format(str(num_nodes)))
            tmp_tree = deepcopy(root)
            delete_from_dic(bigram, i, num_nodes, to_traverse, tmp_tree, ast_tree) 
            num_nodes -= 1

if __name__ == "__main__":
    test_num = 1000
    unigram, bigram = read_dictionary()
    print("Cleaning Starts...")
    with open(train_file_path, 'r') as f:
        raw_data = f.readlines()
        for idx, line in enumerate(raw_data):
            if idx > test_num:
                break
            if idx % 10 == 0:
                print("{} function cleaned".format(str(idx)))
            ast_tree = ast.literal_eval(line)
            cleaning(unigram, bigram, ast_tree)
    print(tot_delete)
    replace_dictionary(bigram)
