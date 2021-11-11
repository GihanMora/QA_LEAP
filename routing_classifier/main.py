import pandas as pd

from routing_classifier.predict_bert import predict_class_bert
from routing_classifier.predict_spacy import predict_class_spacy

embedding_space_bert = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\routing_classifier\embedding_spaces\embedding_space_bert.csv")
embedding_space_spacy = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\routing_classifier\embedding_spaces\embedding_space_spacy.csv")


query_list = ['what is the energy consumption of library?']
for q in query_list:
    predict_class_bert(q,embedding_space_bert)
    predict_class_spacy(q,embedding_space_spacy)