from gensim.models import KeyedVectors

model = KeyedVectors.load('./wv_model/vectors.kv')
ans = model.wv.most_similar(positive=['[{\"type\": \"FunctionDef\", \"children\": [1, 2, 3]}, {\"type\": \"arguments\"}, {\"type\": \"body\"}, {\"type\": \"decorator_list\"}]'])
print(ans)
