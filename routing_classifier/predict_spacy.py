import ast
import string

from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import en_core_web_md
nlp = en_core_web_md.load()

import numpy as np

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.replace('\n', ' ')
    text = ' '.join(text.split())  # remove multiple whitespaces
    return text

def embed(tokens, nlp):
    """Return the centroid of the embeddings for the given tokens.

    Out-of-vocabulary tokens are cast aside. Stop words are also
    discarded. An array of 0s is returned if none of the tokens
    are valid.

    """

    lexemes = (nlp.vocab[token] for token in tokens)

    vectors = np.asarray([
        lexeme.vector
        for lexeme in lexemes
        if lexeme.has_vector
        and not lexeme.is_stop
        and len(lexeme.text) > 1
    ])

    if len(vectors) > 0:
        centroid = vectors.mean(axis=0)
    else:
        width = nlp.meta['vectors']['width']  # typically 300
        centroid = np.zeros(width)

    return centroid



def predict_class_spacy(tokens,embedding_space):
    print(tokens)
    # print(embedding_space)
    sentence_emb = embed(tokens,nlp)
    print(sentence_emb)
    tuples = []
    for i,row in embedding_space.iterrows():
        print(row['classes'])

        dis = cosine_similarity(ast.literal_eval(row['embeddings']), [sentence_emb])
        tuples.append([row['classes'], dis])
    s_tup = sorted(tuples, key=lambda x: x[1])  # sort tuples based on the cosine distance
    print(s_tup)

embedding_space_spacy = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\routing_classifier\embedding_spaces\embedding_space_spacy.csv")
doc = 'go to the building page'
doc = clean_text(doc)
tokens = doc.split(' ')[:50]
predict_class_spacy(tokens,embedding_space_spacy)