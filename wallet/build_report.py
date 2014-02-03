#annual summaries


import pandas as pd
import numpy as np
import matplotlib.pyplot as pylab
import os
import hashlib
import re
from datetime import datetime as dt
from StringIO import StringIO
import subprocess

def build_wallet(dataframe):
	'''
	creates/updates a wallet column in the dataframe based upon the txt files in ./wallet
	'''
	wallets = [a for a in os.listdir('./wallets') if a[-3:] == 'csv']
	bools = {}
	for file in wallets:
		key = file[:-4]
		reg = open('./wallets/'+file, 'r').read().strip().replace('\n','|')
		bools[key] = dataframe.desc.str.contains(reg)
	dataframe['wallet'] = 'unallocated'
	for key in bools.keys():
		dataframe['wallet'][bools[key]] = key
		
	return dataframe


#define some paths
cwd = os.getcwd()
print cwd

#scan import folder for csvs
filelist = [cwd+'/csv/'+a for a in os.listdir(cwd+'/csv/') if a.lower()[-4:] == '.csv']

#import current database
data = [] 

#loop over all csv files found
for index, file in enumerate(filelist):
	#strip account name from filename
	account = re.findall(r'\w+-', file)[-1][:-1]
	print account
	#check for a viable filename
	if account not in ['veridian', 'mastercard', 'visa', 'savings']:
		print 'unable to parse filename - skipping'
		continue

	#read in csvs
	holder = pd.read_csv(file, names=['date', 'amount', 'desc'], delimiter=',', usecols=[0,1,2])
	holder['account'] = account	
	
	data.append(holder)

data = pd.concat(data) #build master frame
data.date = pd.to_datetime(data.date, dayfirst=True) #reformat date column
data = data.set_index('date', drop=False)
data = build_wallet(data) #add wallet definitions

#build calander	
checkpoints = pd.date_range('2012-07-01', periods=18, freq='MS')
ncheckpoints =  len(checkpoints) - 1

#view of incomes
income = data[(data.amount > 0) & (data.wallet != 'transfers')]

#view of costs
costs = data[(data.amount < 0) & (data.wallet != 'transfers')]
costs['amount'] *= -1

sorted = data.sort(columns=['amount'], ascending=False)

print sorted[sorted['wallet'] == 'unallocated'].desc 


#summary of all costs since start, on a per monthly bases
##########################################
cost_summary = []
income_summary = []
columns = []
for key, grp in costs.groupby(['wallet']):
	columns.append(key)
	cost_summary.append(grp.resample('M', how=sum))
summary = pd.concat(cost_summary, axis=1, keys=columns)
income_summary = income.resample("M", how='sum')




#stacked barchart
fig = pylab.figure(figsize=(8.27,11.69))
ax1 = fig.add_subplot(111)
pylab.plot(np.arange(len(income_summary.amount.values))+0.5, income_summary.amount.values, label='total income')
summary.plot(ax=ax1, x = summary.index.month, kind='bar', stacked=True)
handles, labels = pylab.gca().get_legend_handles_labels()
pylab.legend(handles[::-1], labels[::-1], loc=9, labelspacing=0.2, prop={'size':10})
pylab.title("Summary of all expenses.")
pylab.xlabel('Month (2012-2013)')
pylab.ylabel("Amount ($)")
pylab.tight_layout()

pylab.savefig('all_expenses_summary.pdf')
############################################

#total income vs cost since start, on a per month bases
############################################

fig = pylab.figure(figsize=(8.27,11.69))
axes = [fig.add_subplot(311),fig.add_subplot(312),fig.add_subplot(313)]
#~ fig, axes = pylab.subplots(nrows=3, ncols=1)
data.resample('M', how=sum).plot(ax=axes[0], kind='bar')
axes[0].axes.get_xaxis().set_visible(False)
axes[0].set_title('Total Monthly Income')
axes[0].set_ylim(-6000,6000)

df =  pd.concat([income.resample('M', how=sum), costs.resample('M', how=sum)], axis=1)
df.columns = ['income', 'costs']
df.plot(ax=axes[1], kind='bar', color=['k', 'r'])
axes[1].axes.get_xaxis().set_visible(False)
axes[1].set_title('Monthly Income Vs Cost')
axes[1].set_ylim(0,12000)

data.resample('M', how=sum).cumsum().plot(ax=axes[2])
axes[2].set_title('Cumulative Monthly Income')
axes[2].set_ylim(-10000,10000)

fig.tight_layout()
pylab.savefig('all_profit_loss_summary.pdf')
##########################################


#side by side bar chart
fig = pylab.figure(figsize=(8.27,11.69))
ax1 = fig.add_subplot(111)
summary.plot(ax=ax1, x = summary.index.month, kind='bar', legend=False)
handles, labels = pylab.gca().get_legend_handles_labels()
#~ pylab.legend(handles[::-1], labels[::-1], loc=9, labelspacing=0.2, prop={'size':10})
for index, rects in enumerate(ax1.containers):
	for  rect in rects:
		height = rect.get_height()
		if not np.isnan(height):
			txt = labels[index].split(',')[0][1:]
			ax1.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%s'%(txt),
				ha='center', va='bottom', rotation='vertical', size=8)
pylab.title("Summary of all expenses.")
pylab.xlabel('Month (2012-2013)')
pylab.ylabel("Amount ($)")
pylab.tight_layout()


pylab.show()


#annual wallet pie chart
plot_amounts = []
plot_labels = []
for name, group in costs.groupby('wallet'):
	plot_labels.append(name)
	plot_amounts.append(group.amount.sum())

plot_amounts = np.array(plot_amounts)
plot_labels =np.array(plot_labels)
plot_labels = plot_labels[plot_amounts > 1000]
plot_amounts = plot_amounts[plot_amounts > 1000]

pylab.figure()
pylab.pie(plot_amounts, labels=plot_labels, autopct='%1.1f%%', shadow=True, startangle=90, colors=('b', 'g', 'r', 'c', 'm', 'y'),)
pylab.title("Breakdown of all major costs since 1st july 2012")
pylab.savefig('total_cost_pie.pdf')

plot_amounts = []
plot_labels = []
for name, group in income.groupby('wallet'):
	plot_labels.append(name)
	plot_amounts.append(group.amount.sum())

plot_amounts = np.array(plot_amounts)
plot_labels =np.array(plot_labels)
plot_labels = plot_labels[plot_amounts > 1000]
plot_amounts = plot_amounts[plot_amounts > 1000]

pylab.figure()
pylab.pie(plot_amounts, labels=plot_labels, autopct='%1.1f%%', shadow=True, startangle=90, colors=('b', 'g', 'r', 'c', 'm', 'y'),)
pylab.title("Breakdown of all major income sources since 1st july 2012")
pylab.savefig('total_income_pie.pdf')


#individual wallet summaries
#~ for name, group in costs.groupby('wallet'):

	#~ plot_amounts = []
	#~ plot_labels = []
	#~ for item, batch in group.groupby('desc'):
		#~ plot_amounts.append(batch.amount.sum())
		#~ plot_labels.append(item)
		
	#~ ind = np.argsort(plot_amounts)
	#~ plot_amounts = np.take(np.array(plot_amounts), ind)[::-1][:10]
	#~ plot_labels = 	np.take(np.array(plot_labels), ind)[::-1][:10]
	#~ pylab.figure()
	#~ pylab.pie(plot_amounts, labels=plot_labels, autopct='%1.1f%%', shadow=True, startangle=90, colors=('b', 'g', 'r', 'c', 'm', 'y'),)
	#~ pylab.title(name)


monthly_costs = costs.groupby([ lambda x: x.year, lambda x: x.month])
october2013 = monthly_costs.get_group((2013, 9))

# monthly wallet pie chart
plot_amounts = []
plot_labels = []
for name, group in october2013.groupby('wallet'):
	plot_labels.append(name)
	plot_amounts.append(group.amount.sum())

plot_amounts = np.array(plot_amounts)
plot_labels =np.array(plot_labels)

pylab.figure()
pylab.pie(plot_amounts, labels=plot_labels, autopct='%1.1f%%', shadow=True, startangle=90, colors=('b', 'g', 'r', 'c', 'm', 'y'),)
pylab.title("Breakdown of all major costs for October 2013")
pylab.savefig('oct2013_cost_pie.pdf')

#~ plot_amounts = []
#~ plot_labels = []
#~ for name, group in income.groupby('wallet'):
	#~ plot_labels.append(name)
	#~ plot_amounts.append(group.amount.sum())

#~ plot_amounts = np.array(plot_amounts)
#~ plot_labels =np.array(plot_labels)
#~ plot_labels = plot_labels[plot_amounts > 1000]
#~ plot_amounts = plot_amounts[plot_amounts > 1000]

#~ pylab.figure()
#~ pylab.pie(plot_amounts, labels=plot_labels, autopct='%1.1f%%', shadow=True, startangle=90, colors=('b', 'g', 'r', 'c', 'm', 'y'),)
#~ pylab.title("Breakdown of all major income sources for October 2013")
#~ pylab.savefig('oct2013_income_pie.pdf')


#individual wallet summaries
#~ total_costs = october2013.sum()['amount']
#~ for name, group in october2013.groupby('wallet'):

for name, group in costs.groupby('wallet'):
	plot_amounts = []
	plot_labels = []
	for item, batch in group.groupby('desc'):
		plot_amounts.append(batch.amount.sum())
		plot_labels.append(item)
		
	ind = np.argsort(plot_amounts)
	plot_amounts = np.take(np.array(plot_amounts), ind)[::-1]
	plot_labels = 	np.take(np.array(plot_labels), ind)[::-1]
	pylab.figure()
	pylab.pie(plot_amounts, labels=plot_labels, autopct='%1.1f%%', shadow=True, startangle=90, colors=('b', 'g', 'r', 'c', 'm', 'y'),)
	pylab.title(name)
	#~ fig = pylab.figure(figsize=(8.27,11.69))
	#~ ax1 = fig.add_subplot(111)
	#~ summary.plot(ax=ax1, x = summary.index.month, kind='bar', legend=False)
	

pylab.show()





#~ fig, axes = pylab.subplots(nrows=2, ncols=1)
#~ group.resample('M', how=sum).plot(kind='bar',ax=axes[0])
#~ axes[0].set_title(name)
#~ group.resample('M', how=sum).fillna(0).cumsum().plot(ax=axes[1])

#~ monthly_summary = {} 

#~ profit_loss = []
#~ duration = []

#~ for i in range(ncheckpoints): #build monthly summaries and wallets
	#~ start = checkpoints[i]
	#~ end = checkpoints[i+1]
	#~ duration.append((end - start).days)
	#~ print start.month
	#~ print duration
	#~ monthly_data = data[(data.date > start) & (data.date < end)]
	#~ print ''
	
	#========================
	# monthly reviews
	#========================
	# for each month calculate total income and expenditures
	# then split the monthy dataset into wallets
	# for each month plot
	#	total income vs total expenditure (bar graph)
	#	breakdown of total income vs total expenditure (pie charts)
	
	
	#~ monthly_slice = data[(data.date > start) & (data.date < end)]
	#~ groups = monthly_slice.groupby('wallet')
	
	#~ for key in groups.groups.keys():
		#~ print key
	
	#~ monthly_summary[start] = 
	
	
#~ pylab.show()	
	#~ monthly_costs = monthly_slice[monthly_slice.amount < 0]
	#~ monthly_incomes = monthly_slice[monthly_slice.amount > 0]
	
	#~ profit_loss.append(monthly_costs.amount.sum() + monthly_incomes.amount.sum())


#~ pylab.bar(checkpoints[:-1], profit_loss, width=duration, label='profit/loss')
#~ pylab.plot(checkpoints[:-1]+1, np.cumsum(profit_loss), color='k', lw=2, label='cumulative')
#~ pylab.grid()
#~ pylab.xlabel('month')
#~ pylab.ylabel('profit/loss ($)')
#~ pylab.title('Monthy Profit/Loss and Running Total')
#~ pylab.legend(loc='best')
#~ pylab.show()
	
	
	#~ dataset[start] = {'costs': build_wallet(monthly_costs), 'incomes': build_wallet(monthly_incomes)}
	
#~ tmp =  dataset.keys()[1]

#~ print dataset[tmp]['costs']['unallocated']




#~ start_date = "24-9-2013"
		
#~ recent =  data[pd.to_datetime(data.date, dayfirst=True) > pd.to_datetime(start_date, dayfirst=True)]
#~ duration = int((pd.to_datetime(data.date, dayfirst=True).max() -  pd.to_datetime(start_date, dayfirst=True)).days)


	


#~ print ''


#~ document = """\\documentclass{{report}}

#~ \\usepackage[pdftex]{{graphicx}}
#~ \\usepackage[margin=1in]{{geometry}}
#~ \\usepackage{{booktabs}}
#~ \\usepackage{{soul}}
#~ \\title{{ {title} }}
#~ \\author{{ {author} }}
#~ \\begin{{document}}
#~ \\maketitle
#~ \\tableofcontents
#~ \\newpage
#~ \\section{{Summary}}
#~ This document summarises expenditure since last pay.

#~ \\begin{{table}}[h]
#~ \\centering
#~ \\begin{{tabular}}{{cc}}
#~ start &  {start}   \\\\
#~ finish & {finish}  \\\\
 #~ & \\\\
#~ spent total &  {s_total} \\\\
#~ spent / day & \hl{{ {s_day} }}\\\\
 #~ & \\\\
#~ income total & {i_total} \\\\
#~ income / day &  \\hl{{ {i_day} }} \\\\
#~ \\end{{tabular}}
#~ \\end{{table}}
#~ \\newpage

#~ """

#~ info = {
#~ 'title': 'Household Expenditure Review',
#~ 'author': 'S. Fletcher',
#~ 'start':  start_date,
#~ 'finish': "14-10-2013",
#~ 's_total': '\$%.2f' %-recent.amount.sum(),
#~ 's_day': '\$%.2f' %(-recent.amount.sum()/duration),
#~ 'i_total' : '\$4067.53',
#~ 'i_day': '\$%.2f' %(4067.53/31),
#~ }
#~ document = document.format(**info)
#~ keylist = wallet.keys()
#~ keylist.remove('transfers')
#~ keylist.remove('exclude')

#~ plot_labels = []
#~ plot_amounts = []
#~ total_amounts = []
#~ for key in keylist:
	#~ document += '\\section{%s}\n' %key
	#~ document += recent[wallet[key]].to_latex().replace('#','')
	#~ document += '\\newline\n'
	#~ document +=  'Total: \$%.2f \\newline\n' %(recent[wallet[key]].amount.sum())
	#~ document += 'Per day: \$%.2f\n' %(recent[wallet[key]].amount.sum()/31.)
	#~ document += '\\newpage\n\n'
	
	
	#~ plot_labels.append(key)
	#~ plot_amounts.append(recent[wallet[key]].amount.sum())
	#~ total_amounts.append(data[wallet[key]].amount.sum())
	
#~ plot_amounts = np.array(plot_amounts)/-4067	
#~ total_amounts = np.array(total_amounts)/np.sum(total_amounts)

#~ pylab.pie(plot_amounts, labels=plot_labels, autopct='%1.1f%%', shadow=True, startangle=90, colors=('b', 'g', 'r', 'c', 'm', 'y'),)
#~ pylab.savefig('pie.pdf')

#~ pylab.figure()
#~ recent = recent[~wallet['exclude'] & ~wallet['transfers']]
#~ recent.date =pd.to_datetime(recent['date'], dayfirst=True) 
#~ recent = recent.sort('date')
#~ recent['cumsum'] = -recent.amount.cumsum()
#~ recent.plot(x='date', y='cumsum', kind='bar', label='actual')
#~ pylab.gcf().autofmt_xdate()
#~ ax = pylab.gca()
#~ ax.set_xticklabels([], minor=False)
#~ ax.plot([0,92], [131, 31*131], lw=2, color='k', label='required')
#~ pylab.legend(loc='best')
#~ pylab.title('Running sum of expenditure over time')
#~ pylab.xlabel('date')
#~ pylab.ylabel('total spent')
#~ pylab.ylim(0, 4000)
#~ pylab.xlim(0, 90)
#~ pylab.savefig('bar.pdf')

#~ document += '''
#~ \\begin{figure}[p]
#~ \\centering
#~ \\includegraphics[width=0.8\\textwidth]{pie.pdf}
#~ \\caption{Pie chart of expenditures since last pay}
#~ \\label{fig:pie}
#~ \\end{figure}
#~ \\begin{figure}[p]
#~ \\centering
#~ \\includegraphics[width=0.8\\textwidth]{bar.pdf}
#~ \\caption{Rate of Expenditure}
#~ \\label{fig:rate}
#~ \\end{figure}
#~ \\end{document}
#~ '''

	
#~ open('budget.tex', 'w').write(document)

#~ subprocess.call('pdflatex budget.tex', shell=True)




	

#~ 

#~ 
#~ pylab.show()


#~ print pd.to_datetime(['10/10/2013'], dayfirst=True)

	
	#~ data[account] = 
	
	#~ if data[account]: print True
		
	#append to appropriate tables
	#~ ???
	
	#~ tmp = data.get(account, [])
	#~ tmp.append(store)
	#~ data[account] = pd.concat(tmp)




#~ 
#update unique key
#~ keylist = data.date.astype(np.int64).astype(np.str) +  \
#~ data.amount.astype(np.str) + \
#~ data.desc.astype(np.str) + \
#~ data.total.astype(np.str)
#~ data['id'] = keylist.map(lambda x: hashlib.md5(x).hexdigest())
	
#~ idlist = list(data.id.values)
	
#~ print len(idlist)
#~ print len(list(set(idlist)))

#~ store = pd.HDFStore('budget.h5')
#~ store.append('accounts', data, data_columns=['date', 'id', 'amount', 'desc']) 

#~ print store['/accounts/veridian'].head()
#~ print store	






#append to appropriate tables if unique