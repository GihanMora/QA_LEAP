from tableqa.agent import Agent
import pandas as pd
from tableqa.agent import Agent

data_dict = {'Building':['library','lims1','lims2'],'CO2 Emission YTD(tonnes CO2-e)':[1145.09,1391.36,980.40], 'Estimated Cost(AUD)':[953157.27,837971.05,510707.94], 'Energy Usage YTD(kWh)':[1070176.41,18469.24,916264.00],'Consumption Compared to Last Year(%)': [-10.66,+5.53,-0.43]}



df = pd.DataFrame(data_dict)
df.head()


agent = Agent(df)

def qa(query):
  print(agent.query_db(query))
  print(agent.get_query(query))

qa("which building has highest CO2 Emission YTD(tonnes CO2-e)?")