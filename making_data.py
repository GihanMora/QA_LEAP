import random
random.seed(10)
b_list = ['LV_Incoming_TER_EH1', 'LV_Incoming_TER_EM', 'LV_Incoming_TER_EMA', 'LV_Incoming_TER_EMB', 'LV_Incoming_TER_EMC', 'LV_Incoming_TER_EMD', 'LV_Incoming_TER_EME', 'LV_Incoming_TER_MDB_LT_GSM', 'LV_Incoming_TER_NR', 'LV_Incoming_TER_NR1', 'LV_Incoming_TER_NR2', 'LV_Incoming_TER_NR3', 'LV_Incoming_TER_NR4', 'Terraces - NR6', 'Terraces - NR7', 'Terraces - NR8', 'Terraces - T10', 'Terraces - T11', 'Terraces - T12', 'Terraces - T13', 'Terraces - T14', 'Terraces - T7', 'Terraces - T8', 'Terraces - T9', 'HS1 Public Lighting', 'L Public Lighting', 'ISC Public Lighting', 'MC Public Lighting', 'TC Public Lighting', 'U Public Lighting', 'Mont Park', 'TCI Agora East  Virtualised', 'TCI Animal_and_Glass Houses Virtualised', 'CD Agricultural Reserve Virtualised', 'LV_Incoming_BEN_AS2.AS1_Main_Switch', 'LV_Incoming_BEN_AS2.AS2_Main_Switch', 'TCI Agora Theatre  Virtualised', 'LV_Incoming_WOD_SMSB.AW-1_Main_Supply', 'Albury-Wodonga - B1 Virtualised', 'Albury-Wodonga - B3 Virtualised', 'Albury-Wodonga - B3A Virtualised', 'Albury-Wodonga - B4 Virtualised', 'Albury-Wodonga - B5A Virtualised', 'Albury-Wodonga - B6 Virtualised', 'Albury-Wodonga - B8 Virtualised', 'TCI Boilerhouse Virtualised', 'TCI Beth Gleeson Virtualised', 'LV_Incoming_MIL.BGR_Main_Supply', 'TCI BS1 Virtualised', 'TCI BS2 Virtualised', 'CD Childrens Centre Virtualised', 'CD Chisholm College Virtualised', 'TCI CS CS1 CS2 CS3 Virtualised', 'TCI David Myers  Virtualised', 'TCI Donald Whitehead Virtualised', 'TCI ED1 HEUD Virtualised', 'TCI ED2 Virtualised', 'TCI Eastern Lecture Theatre  Virtualised', 'CD Glenn College Virtualised', 'TCI George Singer Virtualised', 'TCI Health Sciences123 Virtualised', 'CD Health Sciences Clinic Virtualised', 'TCI Hooper Szental Virtualised', 'TCI Humanities2 Virtualised', 'TCI Humanities3 Virtualised', 'TCI Indoor Sports Centre Virtualised', 'CD John Scott Meeting House Virtualised', 'TCI Library Virtualised', 'TCI LIMS1 Virtualised', 'TCI LIMS2 Virtualised', 'CD Latrobe Uni Mediucal Centre Virtualised', 'CD Wildlife Reserve Virtualised', 'TCI Martin Virtualised', 'CD Menzies College Main Supply Virtualised', 'CD Menzies College Annexe Virtualised', 'Albury-Wodonga - MH1 Virtualised', 'Albury-Wodonga - MH2 Virtualised', 'TCI Peribolos East Virtualised', 'TCI Physical Sciences1 Virtualised', 'TCI Physical Sciences2 Virtualised', 'TCI Peribolos West Virtualised', 'TCI RLR Virtualised', 'TCI SPF Specialised Pathogen Facility Virtualised', 'LV_Incoming_SHS.SHS_Main_Supply', 'CD SFP Virtualised', 'CD SFP2 Virtualised', 'TCI Social Sciences Virtualised', 'TCI Sylvia Walton Virtualised', 'TCI Thomas Cherry_Shared Virtualised', 'TCI Thomas Cherry Virtualised', 'TCI The Learning Common Virtualised', 'CD Union Virtualised', 'CD Zoological Reserve Virtualised']
# b_list = list(b_list)
# print(type(b_list))
b_new = []
max_pk_consumption = []
total_ytd = []
total_mdt = []
total_wtd = []
cost_dff_baseline = []
estimated_cost = []
co2_ytd= []

for b in b_list:
    # print(i)
    b=b.replace('TCI','').replace('Virtualised','').replace('CD','')
    b_new.append(b.strip())
    total_ytd.append(round(random.uniform(3000000, 7000000), 2))
    total_mdt.append(round(random.uniform(12000, 30000), 2))
    total_wtd.append(round(random.uniform(4000, 12000), 2))
    max_pk_consumption.append(round(random.uniform(3000, 5000), 2))
    cost_dff_baseline.append(round(random.uniform(40000, 60000), 2))
    estimated_cost.append(round(random.uniform(300000, 600000), 2))
    co2_ytd.append(round(random.uniform(500, 1000), 2))



print(b_new)
print(total_ytd)
print(total_mdt)
print(total_wtd)
print(cost_dff_baseline)
print(estimated_cost)
print(co2_ytd)
print(max_pk_consumption)

import pandas as pd

out_df = pd.DataFrame()
out_df['Building'] = b_new
out_df['Total_Energy_Usage_YTD'] = total_ytd
out_df['Total_Energy_Usage_MTD'] = total_mdt
out_df['Total_Energy_Usage_WTD'] = total_wtd
out_df['Cost_Difference_with_Baseline'] = cost_dff_baseline
out_df['Estimated_Total_Cost'] = estimated_cost
out_df['CO2_Emission_YTD'] = co2_ytd
out_df['Maximum_Peak_Energy_Consumption'] = max_pk_consumption

out_df.to_csv(r"E:\Projects\LEAP_Gihan\QA_LEAP\data_tables\\building_data.csv")