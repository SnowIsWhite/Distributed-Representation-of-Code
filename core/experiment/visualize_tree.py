import os
os.environ['QT_QPA_PLATFORM']='offscreen'
import ast
from ete3 import Tree, TreeStyle, TextFace, add_face_to_node

def tree2img(newick_tree, save_path):
    t = Tree(newick_tree, format=1)
    ts = TreeStyle()
    ts.show_leaf_name = False
    ts.show_branch_length = False
    ts.show_branch_support = False
    def my_layout(node):
        F = TextFace(node.name, tight_text=True)
        add_face_to_node(F, node, column=0, position="branch-right")
    ts.layout_fn = my_layout
    ts.branch_vertical_margin = 10
    ts.rotation = 90
    t.render(save_path+'png', tree_style=ts)
    t.render(save_path+'svg', tree_style=ts)

def __make_word(t, tree):
    word = ''
    word += tree[t[0]]['type']
    if 'value' in tree[t[0]] and tree[t[0]]['type'] != 'Str':
        word += ' / '
        word += tree[t[0]]['value']
    return word

def convert_to_newick(str_tree):
    tree = ast.literal_eval(str_tree)
    mStack = []
    tStack = []
    str = ''
    level = 0
    max_level = -1
    mStack.append((0,level))
    while len(mStack)!=0:
        m = mStack.pop()
        level = m[1]
        tStack.append(m)
        if 'children' not in tree[m[0]]:
            t = tStack.pop()
            word = __make_word(t, tree)
            str += word
            if len(mStack) != 0:
                if mStack[-1][1] == t[1]:
                    str += ','
                else:
                    while mStack[-1][1] != tStack[-1][1]:
                        str += ')'
                        # one from t
                        t = tStack.pop()
                        str += __make_word(t, tree)
                    str += ')'
                    t = tStack.pop()
                    str += __make_word(t, tree)
                    str += ','
            else:
                while len(tStack) != 0:
                    str += ')'
                    t = tStack.pop()
                    str += __make_word(t, tree)
            continue
        level += 1
        if level > max_level:
            max_level = level
        str += '('
        for child in tree[m[0]]['children']:
            mStack.append((child, level))
    str += ';'
    return str

def tree_to_image(num):
    read_path_root = './tree_data/{}'.format(str(num))
    write_path_root = './tree_imgs/{}/'.format(str(num))
    if not os.path.exists('./tree_imgs/{}'.format(str(num))):
        os.mkdir('./tree_imgs/{}'.format(str(num)))

    # read folder
    for roots, dirs, files in os.walk(read_path_root):
        for idx, file in enumerate(files):
            write_num = file.split('.')[0]
            if not os.path.exists(os.path.join(write_path_root, write_num)):
                os.mkdir(os.path.join(write_path_root, write_num))
            each_path_root = os.path.join(write_path_root, write_num)
            file_path = os.path.join(read_path_root, file)
            with open(file_path, 'r') as f:
                data = f.readlines()
            last = len(data)-1
            for j, line in enumerate(data):
                line = line.strip()
                if j == last: continue
                if line == 'UNK': continue
                newick = convert_to_newick(line)
              
                tree2img(newick, os.path.join(each_path_root, '{}.'.format(str(j+1))))

                

if __name__ == "__main__":
    tree_to_image(1)
