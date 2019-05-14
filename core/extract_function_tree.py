import json
import ast
import Queue

class Tree:
    "Generic tree node."
    def __init__(self, name='root', children=None):
        self.type = name
        self.children = []
        self.number = 0
        self.value = None
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.type
    def __value__(self):
        return self.value
    def __num__(self):
        return self.number
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)
    def change_number(self, num):
        self.number = num
    def add_value(self, value):
        self.value = value

def tree_to_string(tree):
    # given one single tree, stringify
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
        if node.__value__() is not None:
            element['value'] = node.__value__()
        if len(node.children)!=0:
            element['children'] = []
            for child in node.children:
                element['children'].append(child.__num__())
            for child in reversed(node.children):
                stack.append(child)
        string_tree.append(element)
    string_tree = json.dumps(string_tree)
    return string_tree

def __build_tree(data, el):
    node = Tree(name=el['type'])
    if 'value' in el:
        node.add_value(el['value'])
    if 'children' not in el:
        return node
    for child in el['children']:
        node.add_child(__build_tree(data, data[child]))
    return node

def extract_function_tree(data):
    vis = [0]*len(data)
    trees = []
    new_trees = []
    for i, el in enumerate(data):
        if el['type'] == 'FunctionDef' and vis[i] == 0:
            vis[i] = 1
            #start building tree
            tree = __build_tree(data, el)
            trees.append(tree)
        vis[i] = 1
    for tree in trees:
        # stringify
        new_trees.append(tree_to_string(tree))
    return new_trees

def write_data(tree, line_num):
    with open('./python100k_train_function.json', 'a') as f:
        f.write(tree)
        f.write('\n')
    with open('./function_extract_progress.txt', 'w') as f:
        f.write(line_num)

if __name__ == "__main__":
    progress = 0
    with open('./function_extract_progress.txt', 'r') as f:
        for line in f.readlines():
            if len(line)!= 0:
                progress = int(line)
    with open('../python150/py150/python100k_train.json', 'r') as f:
        for idx, line in enumerate(f.readlines()):
            if idx < progress:
                continue
            data = ast.literal_eval(line)
            tree = extract_function_tree(data)
            for t in tree:
                write_data(t, str(idx))
