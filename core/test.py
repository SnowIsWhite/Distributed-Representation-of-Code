from gensim.models import KeyedVectors

model = KeyedVectors.load('./wv_model/vectors.kv')
ans = model.wv.most_similar(positive=['[{\"type\": \"Expr\", \"children\": [1]}, {\"type\": \"Call\"}]'])
print(ans)
