import torch
from transformers import AutoModelWithLMHead, AutoTokenizer
import datetime
import pandas as pd
from pandasql import sqldf

t1 = datetime.datetime.now()
tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-wikiSQL")
model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-wikiSQL")
device = "cuda:1" if torch.cuda.is_available() else "cpu"
print(device)
model = model.to(device)
t2 = datetime.datetime.now()
print('time for model loading',(t2-t1))

def get_sql(query):
    input_text = "translate English to SQL: %s </s>" % query

    features = tokenizer([input_text], return_tensors='pt').to(device)

    output = model.generate(input_ids=features['input_ids'],max_length = 150,
                            attention_mask=features['attention_mask'])

    return tokenizer.decode(output[0])


from difflib import get_close_matches



def aggregatorMatches(agri_extract):
    valid_agrigators = ['SUM', 'AVG', 'MAX', 'MIN', 'COUNT', 'None']
    matches = get_close_matches(agri_extract, valid_agrigators,3 ,0.6)
    if(len(matches)):
        best_match = matches[0]
    else:best_match = []

    if(agri_extract.lower() in ['maxi','maximum', 'highest', 'biggest']):best_match = 'MAX'
    if (agri_extract.lower() in ['min', 'minimum', 'lowest','smallest']):best_match = 'MIN'
    # print(best_match)
    return best_match
from dateutil.parser import parse

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False
def columnMatches(valid_columns, column_extract, target_column):
    print('col extract',column_extract)
    columns_extensions = {'Total_Energy_Usage_WTD':['energy week-to-date','energy week to date', 'energy usage WTD', 'total energy week to date']}
    for each_k in list(columns_extensions.keys()):
        valid_columns = valid_columns + columns_extensions[each_k]
    matches = get_close_matches(column_extract, valid_columns,3 ,0.4)
    # # print(matches)
    if(len(matches)):
        for each_k in list(columns_extensions.keys()):
            if(matches[0] in columns_extensions[each_k]):
                return each_k
        return matches[0]
    else: return target_column

    # sim_vect = []
    # # print(valid_value_names)
    # for v in valid_columns:
    #     sig = similar(str(v), str(column_extract))
    #     sim_vect.append([v, sig])
    # sim_vect = sorted(sim_vect, key=lambda l: l[1])
    # return sim_vect[-1]
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def column_value_Matches(valid_value_names, value_extract):
    sim_vect = []
    print(valid_value_names)
    for v in valid_value_names:
        if (str(v).isnumeric()):
            sig = similar(str(v), str(value_extract))
        else:
            sig = similar(str(v).lower(), str(value_extract).lower())
        sim_vect.append([v, sig])

    sim_vect = sorted(sim_vect,key=lambda l:l[1])
    print(sim_vect)
    return sim_vect[-1]
    # try:
    #     matches = get_close_matches(value_extract, valid_value_names,3 ,0.1)
    #     # print(matches)
    #     if (len(matches)):
    #         return matches[0]
    #     else:
    #         return []
    # except Exception:
    #     return []

def post_processing(query,table_name_default, table_df):
    valid_cols = list(table_df.columns)
    table_dict = {}
    for vc in valid_cols:
        table_dict[vc] = list(table_df[vc].unique())
    #removing tokens
    query = query.replace('<pad>','').replace('</s>','')
    # tokens = query.split()
    agg = 'None'
    query_splits = (query.split('SELECT')[1]).split('FROM')
    selecting_col = query_splits[0].strip()
    table_name = query_splits[1].split('WHERE')[0].strip()
    table_name = table_name_default
    has_conditions = False
    target_column = 'Building'

    agg_check = selecting_col.split()[0].strip()
    # print('agg_check',agg_check)
    if (agg_check in ['SUM', 'AVG', 'MAX', 'MIN', 'COUNT']):
        agg = agg_check
        selecting_cols = (' ').join(selecting_col.split()[1:])
        selecting_col = columnMatches(valid_columns=valid_cols, column_extract=selecting_col, target_column=target_column)
    else:
        selecting_col = columnMatches(valid_columns=valid_cols, column_extract=selecting_col,  target_column=target_column)
    agg = aggregatorMatches(agg)

    if('WHERE' in query):
        has_conditions = True
        condition = query_splits[1].split('WHERE')[1].strip()
        condition_slices = condition.split('AND')
        is_between = False
        fixed_condition_slices = []
        for each_cs in condition_slices:
            each_cs = each_cs.strip()
            if ('=' in each_cs):
                splitter = '='
                if(' and ' in each_cs):
                    is_between = True


            elif ('<' in each_cs): splitter = '<'
            elif ('>' in each_cs): splitter = '>'
            elif ('between' in each_cs):
                is_between = True
                splitter = 'between'
            column = each_cs.split(splitter)[0].strip()

            if (column not in ['Name','Type','Title']):
                column = columnMatches(valid_columns=valid_cols, column_extract=column,  target_column=target_column)

            print('Column',column)
            agri_cond = each_cs.split(splitter)[1].strip()

            print('cccccc',agri_cond)
            if(is_between):
                splitter = 'BETWEEN'

            if (agri_cond.isnumeric()):
                fixed_cond = "%s %s %s" % (column, splitter, agri_cond)
            elif(' and ' in agri_cond):
                print('aggg',agri_cond)
                fixed_cond = "%s %s %s" % (column, splitter, agri_cond)

            else:
                agri_cond_out = aggregatorMatches(agri_cond)
                if(len(agri_cond_out)):
                    fixed_cond = "%s %s (SELECT %s(%s) FROM %s)" % (column, splitter, agri_cond_out, column, table_name)
                else:
                    if (column in ['Name','Type','Title']):
                        # agri_cond_out = aggregatorMatches(agri_cond)
                        # target_column = 'Building'
                        agri_outs = []
                        for tdk in list(table_dict.keys()):
                            # if(tdk!=target_column):continue
                            print(tdk+">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                            # print()
                            agri_cond_out = column_value_Matches(table_dict[tdk],agri_cond)
                            print(agri_cond_out)
                            agri_outs.append(agri_cond_out+[tdk])
                        agri_outs = sorted(agri_outs, key=lambda l: l[1])

                        fixed_cond = "%s %s '%s'" % (agri_outs[-1][2], splitter, agri_outs[-1][0])

                    else:
                        agri_cond_out = column_value_Matches(table_dict[column], agri_cond)
                        print(agri_cond_out)
                        fixed_cond = "%s %s '%s'" % (column, splitter, agri_cond_out[0])



            # print('fixed_cond',fixed_cond)
            fixed_condition_slices.append(fixed_cond)
        if (len(fixed_condition_slices) > 1):
            fixed_condition_merged = (" AND ").join(fixed_condition_slices)
        else:
            fixed_condition_merged = fixed_condition_slices[0]

        if (agg == 'None'):
            # fixed_sql_template = "SELECT MAX(column_name) FROM table_name WHERE condition"
            fixed_sql_template = "SELECT %s FROM %s WHERE %s" % (selecting_col, table_name, fixed_condition_merged)
        else:
            fixed_sql_template = "SELECT %s(%s) FROM %s WHERE %s" % (
            agg, selecting_col, table_name, fixed_condition_merged)

    else:
        condition = ''
        fixed_condition_merged = ''

        if (agg == 'None'):
            # fixed_sql_template = "SELECT MAX(column_name) FROM table_name WHERE condition"
            fixed_sql_template = "SELECT %s FROM %s" % (selecting_col, table_name)
        else:
            fixed_sql_template = "SELECT %s(%s) FROM %s" % (agg, selecting_col, table_name)




    print('aggrigation : ',agg)
    print('selecting columns : ',selecting_col)
    print('table : ',table_name)
    print('where condition : ', condition)
    print('fixed where condition : ', fixed_condition_merged)



    print('fixed_sql_template',fixed_sql_template)
    return fixed_sql_template


def qa(question,df):

    table_df = df

    # table_df = df
    t3 = datetime.datetime.now()
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('Ouestion : ',question)
    question = question.replace('within','between')

    query = get_sql(question)

    print('Output from LM : ', query)
    # table_df = df
    # pysqldf = lambda q: sqldf(q, globals())







    table_name_default = 'table_df'
    post_processed_query = post_processing(query,table_name_default,table_df)
    # result = pysqldf(post_processed_query)
    print('Query after post processing : ', post_processed_query)
    result = sqldf(post_processed_query, locals())
    result = [i[0] for i in result.values.tolist()]
    print('Predicted answer : ', result)
    return [query, post_processed_query, result]


# df = pd.DataFrame()
# df['building']  = ['library','lims1','lims2']
# df['Energy'] = [1231,4432,5243]
# #
# table_df = df
# qa(question = "which building has maximum energy?",df='S')
# qa(question = "what is the maximum of energy?",df=table_df)
# qa(question = "what is the average of energy?",df=table_df)
# qa(question = "Number of buildings more than 2200 of energy?",df=table_df)
# qa(question = "What are the buildings more than 2200 of energy?",df=table_df)
# qa(question = "Name the building with the highest Total_Energy_Usage_YTD??",df=table_df)
# qa(question = "What is the energy of library?",df=table_df)

# print(get_sql('What building has the highest Total_Energy_Usage_YTD?'))