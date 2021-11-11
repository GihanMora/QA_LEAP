from scipy import spatial
from sklearn.neighbors import NearestNeighbors
import numpy as np
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(X)

y = np.array([[-3,-2]])
distances, indices = nbrs.kneighbors(y)

print(distances,indices)
import pandas as pd
import ast
embedding_space_word_level = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\routing_classifier\embedding_spaces\embedding_space_bert_wordlevel.csv")
label_names = embedding_space_word_level['token']
label_vectors_list = [ast.literal_eval(i)[0] for i in embedding_space_word_level['embedding']]
# print(np.shape(label_vectors))
# print(label_vectors)

label_vectors = np.array(label_vectors_list)
print(label_vectors.shape)
print(X.shape)

nbrs = NearestNeighbors(n_neighbors=1,metric=spatial.distance.cosine).fit(label_vectors)

y = np.array([label_vectors_list[0]])
distances, indices = nbrs.kneighbors(y, return_distance=True)

print(distances,indices)