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
    t.render(save_path, tree_style=ts)

def __make_word(t, tree):
    word = ''
    word += tree[t[0]]['type']
    if 'value' in tree[t[0]]:
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
    print(str)
    return str

if __name__ == "__main__":
    str_tree = '[{"type": "FunctionDef", "children": [1, 5, 12], "value": "get_pyzmq_frame_buffer"}, {"type": "arguments", "children": [2, 4]}, {"type": "args", "children": [3]}, {"type": "NameParam", "value": "frame"}, {"type": "defaults"}, {"type": "body", "children": [6]}, {"type": "Return", "children": [7]}, {"type": "SubscriptLoad", "children": [8, 11]}, {"type": "AttributeLoad", "children": [9, 10]}, {"type": "NameLoad", "value": "frame"}, {"type": "attr", "value": "buffer"}, {"type": "Slice"}, {"type": "decorator_list"}]'
    newick = convert_to_newick(str_tree)
    tree2img(newick, './out.svg')
