import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
model_path = 'bert-base-uncased'
vocab_path = 'bert-base-uncased'

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)

#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    # print('ime',input_mask_expanded)
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    # print('se',sum_embeddings)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask


def get_mean_pooling_emb(sentences,tokenizer,model):

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    device = "cpu"
    # print('device :',device)
    encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=128, return_tensors='pt').to(device)
    # Compute token embeddings
    with torch.no_grad():
        model = model.to(device)
        model_output = model(**encoded_input)

    sentence_embeddings_raw = mean_pooling(model_output, encoded_input['attention_mask'])
    sentence_embeddings = sentence_embeddings_raw.tolist()

    return sentence_embeddings


def create_embedding_space(seed_lists):
    embedding_space = {}
    for each_key in list(seed_lists.keys()):
        print(each_key)
        seed_list = seed_lists[each_key]
        embedding_list = []
        for wd in seed_list:
            embedding_list.append(get_mean_pooling_emb([wd], tokenizer, model))
        embedding_list_1d = [i[0] for i in embedding_list]
        avg_embedding = np.mean(embedding_list_1d, axis=0)
        embedding_space[each_key] = [avg_embedding.tolist()]
    return embedding_space

#
# navigation_seeds = ['goto','show','go to','open','navigate','dashboard','page','building page','building dashboard','optimization dashboard']
# data_retrieval_seeds = ['what','which','how many','building','maximum peak energy','total energy consumption','cost difference with baseline']
# seed_lists = {'navigation':navigation_seeds,'data_retieval':data_retrieval_seeds}
# embedding_space = create_embedding_space(seed_lists)
#
# embedding_df = pd.DataFrame()
# classes = []
# embeddings = []
# for k in list(embedding_space.keys()):
#     classes.append(k)
#     embeddings.append(embedding_space[k])
# embedding_df['classes'] = classes
# embedding_df['embeddings'] = embeddings
# embedding_df.to_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\routing_classifier\embedding_spaces\\embedding_space_bert.csv")

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

