from datetime import datetime
import pandas as pd
from transformers import AutoModelForTableQuestionAnswering, AutoTokenizer, pipeline
t1 = datetime.now()
# Load model & tokenizer

model = 'navteca/tapas-large-finetuned-wtq'
# model = 'google/tapas-base-finetuned-wtq'

tapas_model = AutoModelForTableQuestionAnswering.from_pretrained(model)
tapas_tokenizer = AutoTokenizer.from_pretrained(model)

# Get predictions
nlp = pipeline('table-question-answering', model=tapas_model, tokenizer=tapas_tokenizer)

# table_df = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\data_tables\building_data.csv")
# qa_df = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\data_tables\question_answer_pairs.csv")
table_df = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\data_tables\building_data_simple_12.csv")
qa_df = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\data_tables\question_answer_pairs_simple_12.csv")
print(table_df.columns)
table = {}

for c in table_df.columns:
    # if(c in ['Building', 'Total Energy Usage YTD','Total Energy Usage MTD', 'Total Energy Usage WTD','Cost Difference with Baseline', 'Estimated Total Cost','CO2 Emission YTD', 'Maximum Peak Energy Consumption']):
    if (c in ['Building', 'Total_Energy_Usage_YTD', 'Total_Energy_Usage_MTD', 'Total_Energy_Usage_WTD', 'Cost_Difference_with_Baseline', 'Estimated_Total_Cost', 'CO2_Emission_YTD', 'Maximum_Peak_Energy_Consumption']):
        table[c] = [str(i) for i in table_df[c].tolist()]

print(table)

t2 = datetime.now()
print('loading model',t2-t1)
def qa(query,table):
    print(query)
    tt1 = datetime.now()
    result = nlp({'table': table,'query':query})
    print(result)
    answer = result['cells']
    if (len(result['cells']) == 1):
        if (result['aggregator'] == 'COUNT'):
            answer = len([i for i in result['cells']])

    if(len(result['cells'])>1):
        if (result['aggregator']=='SUM'):
            try:
                answer = sum([float(i) for i in result['cells']])
            except ValueError:
                answer =  result['cells']
        elif (result['aggregator'] == 'COUNT'):
            answer = len([i for i in result['cells']])
        elif (result['aggregator'] == 'AVERAGE'):
            answer = sum([float(i) for i in result['cells']])/len([i for i in result['cells']])
        elif (result['aggregator'] == 'NONE'):
            answer = result['cells']
        else:
            answer = 'None'

    tt2 = datetime.now()
    print('prediction time', tt2 - tt1)
    return [answer,result]

predictions = []
raw_results = []
for i,row in qa_df.iterrows():
    pred = qa(row['question'],table)
    predictions.append(pred[0])
    raw_results.append(str(pred[1]))
    # break

out_df = qa_df
out_df['predictions'] = predictions
out_df['raw_results'] = raw_results
out_df.to_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\tapas\predictions\\predictions_simlpe_12.csv")
