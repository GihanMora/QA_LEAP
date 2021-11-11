# !pip install transformers
# !pip install torch-scatter -f https://data.pyg.org/whl/torch-1.9.0+${CUDA}.html
from datetime import datetime

from transformers import AutoModelForTableQuestionAnswering, AutoTokenizer, pipeline
t1 = datetime.now()
# Load model & tokenizer

model = 'navteca/tapas-large-finetuned-wtq'
# model = 'google/tapas-base-finetuned-wtq'

tapas_model = AutoModelForTableQuestionAnswering.from_pretrained(model)
tapas_tokenizer = AutoTokenizer.from_pretrained(model)

# Get predictions
nlp = pipeline('table-question-answering', model=tapas_model, tokenizer=tapas_tokenizer)

table = {
      'Building': ['LV_Incoming_TER_EH1_Main_Switch_Real_Energy_Into_the_Load_kWh', 'LV_Incoming_TER_EM_Main_Switch_Real_Energy_Into_the_Load_kWh', 'LV_Incoming_TER_EMA_Main_Switch_Real_Energy_Into_the_Load_kWh', 'LV_Incoming_TER_EMB_Main_Switch_Real_Energy_Into_the_Load_kWh', 'LV_Incoming_TER_EMC_Main_Switch_Real_Energy_Into_the_Load_kWh', 'LV_Incoming_TER_EMD_Main_Switch_Real_Energy_Into_the_Load_kWh', 'LV_Incoming_TER_EME_Main_Switch_Real_Energy_Into_the_Load_kWh', 'LV_Incoming_TER_MDB_LT_GSM_Main_Switch_Real_Energy_Into_the_Load_kWh', 'LV_Incoming_TER_NR_Main_Switch_Real_Energy_Into_the_Load_kWh', 'LV_Incoming_TER_NR1_Main_Switch_Real_Energy_Into_the_Load_kWh', 'LV_Incoming_TER_NR2_Main_Switch_Real_Energy_Into_the_Load_kWh', 'LV_Incoming_TER_NR3_Main_Switch_Real_Energy_Into_the_Load_kWh', 'LV_Incoming_TER_NR4_Main_Switch_Real_Energy_Into_the_Load_kWh', 'Terraces - NR6', 'Terraces - NR7', 'Terraces - NR8', 'Terraces - T10', 'Terraces - T11', 'Terraces - T12', 'Terraces - T13', 'Terraces - T14', 'Terraces - T7', 'Terraces - T8', 'Terraces - T9', 'HS1 Public Lighting', 'L Public Lighting', 'ISC Public Lighting', 'MC Public Lighting', 'TC Public Lighting', 'U Public Lighting', 'Mont Park', 'TCI Agora East Building  Virtualised', 'TCI Animal and Glass Houses Virtualised', 'CD Agricultural Reserve Virtualised', 'LV_Incoming_BEN_AS2.AS1_Main_Switch', 'LV_Incoming_BEN_AS2.AS2_Main_Switch', 'TCI Agora Theatre  Virtualised', 'LV_Incoming_WOD_SMSB.AW-1_Main_Supply', 'Albury-Wodonga - B1 Virtualised', 'Albury-Wodonga - B3 Virtualised', 'Albury-Wodonga - B3A Virtualised', 'Albury-Wodonga - B4 Virtualised', 'Albury-Wodonga - B5A Virtualised', 'Albury-Wodonga - B6 Virtualised', 'Albury-Wodonga - B8 Virtualised', 'TCI Boilerhouse Building Virtualised', 'TCI Beth Gleeson Building Virtualised', 'LV_Incoming_MIL.BGR_Main_Supply', 'TCI BS1 Building Virtualised', 'TCI BS2 Building Virtualised', 'CD Childrens Centre Virtualised', 'CD Chisholm College Virtualised', 'TCI CS Buildings CS1 CS2 CS3 Virtualised', 'TCI David Myers Building  Virtualised', 'TCI Donald Whitehead Building Virtualised', 'TCI ED1 Building HEUD Virtualised', 'TCI ED2 Building Virtualised', 'TCI Eastern Lecture Theatre  Virtualised', 'CD Glenn College Virtualised', 'TCI George Singer Building Virtualised', 'TCI Health Sciences Buildings 1 2 3 Virtualised', 'CD Health Sciences Clinic Virtualised', 'TCI Hooper Szental Building Virtualised', 'TCI Humanities 2 Building Virtualised', 'TCI Humanities 3 Building Virtualised', 'TCI Indoor Sports Centre Virtualised', 'CD John Scott Meeting House Virtualised', 'TCI Library Virtualised', 'TCI LIMS 1 Virtualised', 'TCI LIMS2 Building Virtualised', 'CD Latrobe Uni Mediucal Centre Virtualised', 'CD Wildlife Reserve Virtualised', 'TCI Martin Building Virtualised', 'CD Menzies College Main Supply Virtualised', 'CD Menzies College Annexe Virtualised', 'Albury-Wodonga - MH1 Virtualised', 'Albury-Wodonga - MH2 Virtualised', 'TCI Peribolos East Building Virtualised', 'TCI Physical Sciences 1 Building Virtualised', 'TCI Physical Sciences 2 Building Virtualised', 'TCI Peribolos West Building Virtualised', 'TCI RLR Building Virtualised', 'TCI SPF Specialised Pathogen Facility Virtualised', 'LV_Incoming_SHS.SHS_Main_Supply', 'CD SFP Virtualised', 'CD SFP2 Virtualised', 'TCI Social Sciences Building Virtualised', 'TCI Sylvia Walton Building Virtualised', 'TCI Thomas Cherry Shared Load Virtualised', 'TCI Thomas Cherry Building Virtualised', 'TCI The Learning Commons Building Virtualised', 'CD Union Virtualised', 'CD Zoological Reserve Virtualised'],
      'CO2 Emission YTD': [
          '1145.09',
          '1391.36',
          '980.40'
      ],
      'Estimated Cost': [
          '953157.27',
          '837971.05',
          '510707.94'
      ],
      'Energy Usage YTD': [
          '1070176.41',
          '18469.24',
          '916264.00'
      ],
    'Percentage Consumption Compared to Last Year': [
              '-10.66%',
              '+5.53%',
              '-0.43%'
          ]
  }
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
    return answer

table1 = {
      'Building': [str(i) for i in range(30)],
      'total': [str(i*100) for i in range(30)]
  }

print(qa('What is the total of 30?', table1))


# # #max min average
# # print(">>>>>>>>>>>>>>>>>>>>>>>>")
# print(qa('What is the highest Estimated Cost?'))
# print(qa('What is the lowest CO2 Emission YTD?'))
# # print(qa('What is the highest total?'))
# # print(qa('What is the lowest total?'))
# # print(qa('What is the highest minimum?'))
# # print(qa('What is the lowest minimum?'))
# # # print(">>>>>>>>>>>>>>>>>>>>>>>>")
# print(qa('Which building has highest Estimated Cost?'))
# print(qa('Which building has lowest Energy Usage YTD?'))
# # # print(">>>>>>>>>>>>>>>>>>>>>>>>")
# print(qa('What is the Estimated Cost of library?'))
# print(qa('What is the Percentage Consumption Compared to Last Year of lims1?'))
# # # print(">>>>>>>>>>>>>>>>>>>>>>>>")
# print(qa('What is the sum of Estimated Cost?'))
# print(qa('What is the sum of Energy Usage YTD?'))
# print(qa('What is the average Energy Usage YTD?'))
# print(qa('What is the average Estimated Cost?'))
# # # print(qa('What is the average minimum?'))
# # # print(">>>>>>>>>>>>>>>>>>>>>>>>")
# # print(qa("how many buildnigs are there?"))
# #
# print(qa("Number of buildings more than 500,000 of Estimated Cost?"))
# print(qa("Number of buildings less than 50,000 of Energy Usage YTD?"))
# print(qa("what are buildings less than 50,000 of Energy Usage YTD?"))
# print(qa("What are buildings more than 500,000 of Estimated Cost?"))
# print(qa("What are the buildnigs?"))
# print(qa('What is the sum of total?'))
# print(qa("What are buildings with total between 5000 and 10000?"))
# print(qa("What are buildings between  5000 and 10000 of total?"))


# #max min average
# print(">>>>>>>>>>>>>>>>>>>>>>>>")
# print(qa('What is the highest peak?'))
# print(qa('What is the lowest peak?'))
# # print(qa('What is the highest total?'))
# # print(qa('What is the lowest total?'))
# # print(qa('What is the highest minimum?'))
# # print(qa('What is the lowest minimum?'))
# # print(">>>>>>>>>>>>>>>>>>>>>>>>")
# print(qa('Which building has highest peak?'))
# print(qa('Which building has lowest total?'))
# # print(">>>>>>>>>>>>>>>>>>>>>>>>")
# print(qa('What is the peak of library?'))
# print(qa('What is the minimum of lims1?'))
# # print(">>>>>>>>>>>>>>>>>>>>>>>>")
# print(qa('What is the sum of peaks?'))
# print(qa('What is the sum of totals?'))
# print(qa('What is the average peak?'))
# print(qa('What is the average total?'))
# # print(qa('What is the average minimum?'))
# # print(">>>>>>>>>>>>>>>>>>>>>>>>")
# print(qa("how many buildnigs are there?"))
#
# print(qa("Number of buildings more than 400 of peak?"))
# print(qa("Number of buildings less than 10000 of total?"))
# print(qa("what are buildings less than 400 of peak?"))
# print(qa("What are buildings less than 10000 of total?"))
# print(qa("What are the buildnigs?"))
# print(qa('What is the sum of total?'))
# print(qa("What are buildings with total between 5000 and 10000?"))
# print(qa("What are buildings between  5000 and 10000 of total?"))
ttt2 = datetime.now()
print('Total time', ttt2 - t1)