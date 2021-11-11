import pandas as pd
import ast
# df = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\tapas\predictions\predictions_simlpe_12.csv")
# df = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\T5_experiments\predictions_simple_12.csv")
df = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\T5_experiments\predictions_simple_all.csv")
correct_count = 0
correct_list = []
for i,row in df.iterrows():
    # print(i)
    if(row['predictions']=='Error'):
        pred = 'error'
    else:
        pred = ast.literal_eval(row['predictions'])

    # print(type(pred))
    if(isinstance(pred, list)):
        if(len(pred)==1):
            # print(pred)
            pred = pred[0]
    # print(pred)
    # print(row['answer'])
    ans =  row['answer']
    if('AVG' in row['pred_queries_processed']):
        pred = round(pred,2)
    if ('SUM' in row['pred_queries_processed']):
        pred = round(pred, 2)
        if(str(ans).isnumeric()):
            ans = round(ans, 2)
    if(ans!=str(pred)):
        # print(row)
        correct_count+=1
        correct_list.append(row.to_dict())
print(correct_count)

c_df = pd.DataFrame(correct_list)
c_df.to_csv(r'E:\Projects\LEAP_Gihan\QA_LEAP\T5_experiments\\incorrect_all.csv')

