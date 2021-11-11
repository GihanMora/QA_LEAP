# import spacy
# import spacy.cli
# spacy.cli.download("en_core_web_lg")
# nlp = spacy.load('en_core_web_lg')
import en_core_web_md
from scipy import spatial
from sklearn import neighbors

nlp = en_core_web_md.load()

import numpy as np

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

centroid = embed(['fast','man'],nlp)
print(centroid)
print(centroid.shape)




import string

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.replace('\n', ' ')
    text = ' '.join(text.split())  # remove multiple whitespaces
    return text




label_names = ['navigation', 'entertainment', 'politics', 'sport', 'tech']
doc = "my name is sheela"
doc = clean_text(doc)
label_vectors = np.asarray([embed(label.split(' '), nlp) for label in label_names])
s = [[1,2,3,4],[1,2,3]]
print('dd',np.asarray(s))
print('lv',label_vectors)
tokens = doc.split(' ')
centroid = embed(tokens, nlp)
print('cent',[centroid])
# neigh = neighbors.NearestNeighbors(n_neighbors=1,metric=spatial.distance.cosine)
# neigh.fit(label_vectors)
# closest_label = neigh.kneighbors([centroid], return_distance=False)[0, 0]
# print(label_names[closest_label])


# def predict(doc, nlp, neigh):
#     doc = clean_text(doc)
#     tokens = doc.split(' ')[:50]
#     centroid = embed(tokens, nlp)
#     closest_label = neigh.kneighbors([centroid], return_distance=False)[0][0]
#     return closest_label
#
#
#
#
#
#
#
# preds = [label_names[predict(doc, nlp, neigh)] for doc in docs]

print(embed(['island'],nlp))