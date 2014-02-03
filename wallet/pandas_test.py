import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#testing stuff

#~ file = '../csv/CSVData1.csv'

#~ data = pd.read_csv(file, names=['date', 'amount', 'description', 'total'], delimiter=',')

#~ data.date = pd.to_datetime(pd.Series(data.date), dayfirst=True)

#~ print data['description']

#~ transfers = data[data['description'].str.lower().str.contains("netbank transfer")]

#~ print transfers.tail()

#~ velseis =  data[data['description'].str.lower().str.contains("velseis pty")]

#~ velseis_reimbs = ~velseis['description'].str.lower().str.contains('reimb')

#~ velpays = velseis[velseis_reimbs]

#~ velpays.plot(x='date', y='amount')

#~ for name, group in data.groupby('description'):
	#~ print group
	#~ print ''

#~ data['cumulative'] = data.amount.cumsum()

#~ data.total.plot()

#~ plt.show()

#scan import folder for csvs
#loop over all csv files found
#import each csv file into a working table.
#generate unique key
#append to appropriate tables if unique



