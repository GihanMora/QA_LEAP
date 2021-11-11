import pandas as pd

from T5_experiments.T5_txt_2_sql import qa

import random
import datetime


dates = pd.date_range(start='1/1/2018',end='1/1/2020',  freq='15min')
print(dates)
energy = [round(random.uniform(3000, 7000), 2) for i in range(len(dates))]
print('ssss',energy)
table_df = pd.DataFrame()
table_df['datetime'] = dates
table_df['energy'] = energy

#testing
pred = qa('What is the energy in dates more than "2019-06-01"?',table_df)
# pred = qa('What is the dates and energy in energy more than 5000?',table_df)
