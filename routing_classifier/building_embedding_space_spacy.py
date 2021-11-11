import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
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


def create_embedding_space(seed_lists):
    embedding_space = {}
    for each_key in list(seed_lists.keys()):
        print(each_key)
        seed_list = seed_lists[each_key]
        avg_embedding = embed(seed_list,nlp)
        embedding_space[each_key] = [avg_embedding.tolist()]
    return embedding_space


navigation_seeds = ['goto','show','go to','open','navigate','dashboard','page','building page','building dashboard','optimization dashboard']
data_retrieval_seeds = ['what','which','how many','building','maximum peak energy','total energy consumption','cost difference with baseline']
seed_lists = {'navigation':navigation_seeds,'data_retieval':data_retrieval_seeds}
embedding_space = create_embedding_space(seed_lists)

embedding_df = pd.DataFrame()
classes = []
embeddings = []
for k in list(embedding_space.keys()):
    classes.append(k)
    embeddings.append(embedding_space[k])
embedding_df['classes'] = classes
embedding_df['embeddings'] = embeddings
embedding_df.to_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\routing_classifier\embedding_spaces\\embedding_space_spacy.csv")

#
# print('navi emb',np.shape(embedding_space['navigation']))
# print('navi emb',np.shape(np.sum(embedding_space['navigation'])/len(embedding_space['navigation'])))
#
# navi_emb_list = [i[0] for i in embedding_space['navigation']]
# data_ret_emb_list = [i[0] for i in embedding_space['data_retieval']]
# navigation_avg_embed = np.mean(navi_emb_list, axis=0)
# data_retrieval_avg_embed = np.mean(data_ret_emb_list, axis=0)
# navigation_avg_embed = np.mean(embedding_space['navigation'])
# data_retrieval_avg_embed = np.mean(embedding_space['data_retieval'])

# for na in navi_emb_list:
#     print(na)
#
# print('sss',navigation_avg_embed)
# print(embedding_space['navigation'])

# sentence = "go to building page"
# sentence_emb = get_mean_pooling_emb([sentence], tokenizer, model)
# print(sentence_emb)
# print(np.shape([navigation_avg_embed]))
# print(np.shape(sentence_emb))
#
# print('navi',[navigation_avg_embed.tolist()])
# print('sent',sentence_emb)
#
#
# dis = cosine_similarity([navigation_avg_embed.tolist()], sentence_emb)
# print(dis)
# dis = cosine_similarity([data_retrieval_avg_embed], sentence_emb)
# print(dis)

