import pandas as pd

from T5_experiments.T5_txt_2_sql import qa

table_df = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\data_tables\building_data.csv")
qa_df = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\data_tables\question_answer_pairs.csv")
# table_df = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\data_tables\building_data_simple_12.csv")
# qa_df = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\data_tables\question_answer_pairs_simple_12.csv")

pred_queries = []
pred_queries_processed = []
predictions = []


#testing
# pred = qa('What is the Total_Energy_Usage_WTD of Library?',table_df)
# pred = qa('What is the total energy week to day of Library?',table_df)

# pred = qa('Total_Energy_Usage_WTD of Library?',table_df)
# pred = qa('what is the energy WTD of Library?',table_df)
# pred = qa('Tell me the energy WTD of Library?',table_df)
# pred = qa('Show the energy WTD of Library?',table_df)
# pred = qa('Show the enrgy WTD of Lib?',table_df)
# pred = qa('How much is the Total_Energy_Usage_WTD of Lib?',table_df)
# pred = qa('How much is the WTD energy of Library?',table_df)
pred = qa('How much is the energy in this week of Library?',table_df)
print(sas)


for i,row in qa_df.iterrows():
    # if(i<130):continue
    try:
        pred = qa(row['question'],table_df)
        pred_queries.append(pred[0])
        pred_queries_processed.append(pred[1])
        predictions.append(pred[2])
    except Exception:

        pred_queries.append('Error')
        pred_queries_processed.append('Error')
        predictions.append('Error')
    # break

out_df = qa_df
out_df['predictions'] = predictions
out_df['pred_queries'] = pred_queries
out_df['pred_queries_processed'] = pred_queries_processed

# out_df.to_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\T5_experiments\\predictions_simple_12.csv")
out_df.to_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\T5_experiments\\predictions_simple_all.csv")