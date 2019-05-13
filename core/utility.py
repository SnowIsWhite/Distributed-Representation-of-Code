import json
import ast
unigram_file_path = './one_gram.json'
bigram_file_path = './bigram.json'
bigram_score_path = './bigram_score.json'

def read_bigram():
    with open(bigram_file_path, 'r') as f:
        line = f.readline()
        bigram = ast.literal_eval(line) 
    return bigram

def read_unigram():
    with open(unigram_file_path, 'r') as f:
        line = f.readline()
        unigram = ast.literal_eval(line)
    return unigram

def read_bigram_score():
    with open(bigram_score_path, 'r') as f:
        line = f.readline()
        bigram_score = ast.literal_eval(line)
    return bgiram_score

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


