import pandas as pd
import numpy as np
# df = pd.read_csv(r"E:\Projects\QA_LEAP\data_tables\building_data.csv")
df = pd.read_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\data_tables\building_data.csv")
print(list(df.columns))


# dimensions = ['Building', 'Total Energy Usage YTD', 'Total Energy Usage MTD', 'Total Energy Usage WTD', 'Cost Difference with Baseline', 'Estimated Total Cost', 'CO2 Emission YTD', 'Maximum Peak Energy Consumption']
dimensions = ['Building', 'Total_Energy_Usage_YTD', 'Total_Energy_Usage_MTD', 'Total_Energy_Usage_WTD', 'Cost_Difference_with_Baseline', 'Estimated_Total_Cost', 'CO2_Emission_YTD', 'Maximum_Peak_Energy_Consumption']

qa_pairs = []
#max min average sum
for d in dimensions:
    if(d=='Building'):continue
    qa_pairs.append(["What is the highest "+ d +"?",np.max(df[d].tolist())])
    qa_pairs.append(["What is the lowest " + d + "?",np.min(df[d].tolist())])
    qa_pairs.append(["What is the sum of " + d + "?",np.sum(df[d].tolist())])
    qa_pairs.append(["What is the average of " + d + "?",round(np.average(df[d].tolist()),2)])
    qa_pairs.append(["Name the building with the highest " + d + "?", df.loc[df[d] == np.max(df[d].tolist()), 'Building'].values[0]])
    qa_pairs.append(["Name the building with the lowest " + d + "?", df.loc[df[d] == np.min(df[d].tolist()), 'Building'].values[0]])
    qa_pairs.append(["Number of buildings more than " + str(int(np.quantile(df[d].tolist(), 0.95))) + " of " + d + "?",len(df.loc[df[d] > int(np.quantile(df[d].tolist(), 0.95)), 'Building'].values)])
    qa_pairs.append(["What are the buildings with more than " + str(int(np.quantile(df[d].tolist(), 0.95))) + " of " + d + "?",list(df.loc[df[d] > int(np.quantile(df[d].tolist(), 0.95)), 'Building'].values)])


#retrieve dimentional data from a building
for b in df['Building'].tolist():
    building_row = df.loc[df['Building'] == b]
    for d in dimensions:
        if (d == 'Building'): continue
        qa_pairs.append(["What is the " + d + " of the building "+b+"?",building_row[d].values[0]])

questions = []
answers = []
for qq in qa_pairs:
    print(qq)
    questions.append(qq[0])
    answers.append(qq[1])


out_df = pd.DataFrame()
out_df['question'] = questions
out_df['answer'] = answers

out_df.to_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\data_tables\\question_answer_pairs.csv")


