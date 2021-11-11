import ast

import numpy as np
import pandas as pd
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
from routing_classifier.building_embedding_space_bert import get_mean_pooling_emb

model_path = 'bert-base-uncased'
vocab_path = 'bert-base-uncased'

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)




def predict_class_bert(sentence,embedding_space):
    # print(sentence)
    # print(embedding_space)
    sentence_emb = get_mean_pooling_emb([sentence],tokenizer,model)
    # print(sentence_emb)
    tuples = []
    for i,row in embedding_space.iterrows():
        # print(row['classes'])

        dis = cosine_similarity(ast.literal_eval(row['embeddings']), sentence_emb)
        dis = np.round(dis,3)
        tuples.append([row['classes'], dis])
    s_tup = sorted(tuples, key=lambda x: x[1])  # sort tuples based on the cosine distance
    print(sentence,s_tup)

def predict_class_bert_tokenwise(sentence,embedding_space):
    tokens = sentence.split(' ')
    for token in tokens:
        predict_class_bert(token,embedding_space)

embedding_space = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\routing_classifier\embedding_spaces\embedding_space_bert.csv")
predict_class_bert('what is the energy consumption of library?',embedding_space)
predict_class_bert_tokenwise('what is the energy consumption of library?',embedding_space)