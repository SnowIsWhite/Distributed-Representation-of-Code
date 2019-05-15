import json
import ast
import operator

with open('../bigram_score.json', 'r') as f:
    data = ast.literal_eval(f.readline())

def topk():
    global data
    sorted_dic = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
    k = 5
    print(len(sorted_dic))
    for idx, tup in enumerate(sorted_dic):
        if idx >= k: break
        print(tup[0])
        print(tup[1])

def tree_pmi(target):
    global data
    return data[target]

if __name__ == "__main__":
    with open('./target.txt', 'r') as f:
        target = f.readline()
    target = target.strip()
    pmi = tree_pmi(target)
    print(pmi)
