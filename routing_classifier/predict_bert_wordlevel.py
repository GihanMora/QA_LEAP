import ast

import numpy as np
import pandas as pd
import torch
from scipy import spatial
from sklearn import neighbors
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
from routing_classifier.building_embedding_space_bert import get_mean_pooling_emb

model_path = 'bert-base-uncased'
vocab_path = 'bert-base-uncased'

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)


embedding_space_word_level = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\routing_classifier\embedding_spaces\embedding_space_bert_wordlevel.csv")
label_names = embedding_space_word_level['token']
label_vectors_list = [ast.literal_eval(i)[0] for i in embedding_space_word_level['embedding']]

label_vectors = np.array(label_vectors_list)
neigh = neighbors.NearestNeighbors(n_neighbors=2,metric=spatial.distance.cosine)
neigh.fit(label_vectors)
print('neighb constructed')
def predict_class_bert(sentence):
    # print(sentence)
    # print(embedding_space)
    sentence_emb = get_mean_pooling_emb([sentence],tokenizer,model)
    print(np.shape(sentence_emb))
    print(sentence_emb)
    sentence_emb = np.array(sentence_emb)
    # sentence_emb = sentence_emb.reshape(1, -1)
    # print(sentence_emb)
    s = np.array([label_vectors_list[0]])

    distances, indices = neigh.kneighbors(sentence_emb, return_distance=True)
    # print(label_names[closest_label])
    labels = [label_names[i].tolist() for i in indices]
    print(sentence,labels,distances)

def predict_class_bert_tokenwise(sentence):
    tokens = sentence.split(' ')
    for token in tokens:
        predict_class_bert(token)

embedding_space = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\routing_classifier\embedding_spaces\embedding_space_bert.csv")
predict_class_bert('what is the energy consumption and difference of library?')
predict_class_bert_tokenwise('what is the energy consumption of library')