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
      'Building': [
          'library',
          'lims1',
          'lims2'
      ],
      'Peak': [
          '365',
          '451',
          '393'
      ],
      'minimum': [
          '51',
          '77',
          '34'
      ],
      'total': [
          '11000',
          '12341',
          '9341'
      ]
  }
t2 = datetime.now()
print('loading model',t2-t1)
def qa(query):
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

#max min average
print(">>>>>>>>>>>>>>>>>>>>>>>>")
print(qa('What is the highest peak?'))
print(qa('What is the lowest peak?'))
# print(qa('What is the highest total?'))
# print(qa('What is the lowest total?'))
# print(qa('What is the highest minimum?'))
# print(qa('What is the lowest minimum?'))
# print(">>>>>>>>>>>>>>>>>>>>>>>>")
print(qa('Which building has highest peak?'))
print(qa('Which building has lowest total?'))
# print(">>>>>>>>>>>>>>>>>>>>>>>>")
print(qa('What is the peak of library?'))
print(qa('What is the minimum of lims1?'))
# print(">>>>>>>>>>>>>>>>>>>>>>>>")
print(qa('What is the sum of peaks?'))
print(qa('What is the sum of totals?'))
print(qa('What is the average peak?'))
print(qa('What is the average total?'))
# print(qa('What is the average minimum?'))
# print(">>>>>>>>>>>>>>>>>>>>>>>>")
print(qa("how many buildnigs are there?"))

print(qa("Number of buildings more than 400 of peak?"))
print(qa("Number of buildings less than 10000 of total?"))
print(qa("what are buildings less than 400 of peak?"))
print(qa("What are buildings less than 10000 of total?"))
print(qa("What are the buildnigs?"))
# print(qa('What is the sum of total?'))

ttt2 = datetime.now()
print('Total time', ttt2 - t1)