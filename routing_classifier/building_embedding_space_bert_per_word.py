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

    # device = "cuda:0" if torch.cuda.is_available() else "cpu"
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


def create_embedding_space_wordlevel(seed_lists):
    tokens = []
    embeddings = []
    classes = []
    for each_key in list(seed_lists.keys()):
        print(each_key)
        seed_list = seed_lists[each_key]

        for wd in seed_list:
            embeddings.append(get_mean_pooling_emb([wd], tokenizer, model))
            tokens.append(wd)
            classes.append(each_key)


    emb_df = pd.DataFrame()
    emb_df['token'] = tokens
    emb_df['embedding'] = embeddings
    emb_df['clsas'] = classes
    return emb_df


buildings = ['library','lims1','lims2']
general_seeds = ['is','the','of']
navigation_seeds = ['goto','show','go to','open','navigate','dashboard','page','building page','building dashboard','optimization dashboard']
data_retrieval_seeds = ['what','which','how many','building','maximum peak energy','total energy consumption','cost difference with baseline']
seed_lists = {'buildings':buildings,'general_seeds':general_seeds,'navigation':navigation_seeds,'data_retieval':data_retrieval_seeds}
embedding_space = create_embedding_space_wordlevel(seed_lists)


embedding_space.to_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\routing_classifier\embedding_spaces\\embedding_space_bert_wordlevel.csv")

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

