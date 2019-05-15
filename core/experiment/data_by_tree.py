import os
import ast
import json

file_path = './tree_data/{}/{}.txt'
window = [-3,-2,-1,0,1,2,3]

def check_boundary(index, len_list):
    return index >= 0 and index < len_list

with open('./target.txt', 'r') as f:
    target = f.readline().strip()

with open('../tokenized_data_bigram.json', 'r') as f:
    tokenized_data = ast.literal_eval(f.readline())
    # list of list

with open('../python100k_train_function.json', 'r') as f:
    actual_data = f.readlines()    

def write_file(target, num):
    global tokenized_data
    global actual_data
    global window
    if not os.path.exists('./tree_data/{}'.format(str(num))):
        os.mkdir('./tree_data/{}'.format(str(num)))
    cnt = 1
    for i, sentence in enumerate(tokenized_data):
        writes = []
        if target in sentence:
            for j, word in enumerate(sentence):
                if target == word:
                    for k in window:
                        if check_boundary(j+k, len(sentence)):
                            writes.append(sentence[j+k])
            writes.append(actual_data[i])
            with open(file_path.format(str(num), str(cnt)), 'w') as f:
                for w in writes:
                    f.write(w)
                    if w != 'UNK':
                        ast.literal_eval(w)
                    f.write('\n')
            f.close()
            cnt += 1

write_file(target, 1)

