import tables as tb
import numpy as np
import sys
import os


filename = "budget.h5"

['date', 'amount', 'description', 'total']

class _table(tb.IsDescription):
	date		= tb.Time64Col()  # 16-character String
	id 		= tb.Int64Col()      # Signed 64-bit integer
	desc		= tb.StringCol(256)# 256-character String
	amount  	= tb.Float32Col()    # float  (single-precision)
	

if os.path.isfile(filename): 
	print "File Exists! Rename or delete budget.h5 to continue..."
	sys.exit()
else:
	#create database
	h5file = tb.open_file("budget.h5", mode = "w", title = "Budget Database")
	
	#create groups
	accounts = h5file.create_group("/", 'accounts', 'Account Tables')
	wallets = h5file.create_group("/", 'wallets', 'Wallet Tables')
	
	#create account tables
	veridian = h5file.create_table(accounts, 'table', _table, "Veridian Account")
	#~ mastercard = h5file.create_table(accounts, 'mastercard',_table, "Mastercard Account")
	#~ visa = h5file.create_table(accounts, 'visa',_table, "Visa Account")
	#~ savings = h5file.create_table(accounts, 'savings',_table, "Savings Account")
	
	#create wallet tables
	#~ groceries = h5file.create_table(wallets, 'groceries',_table, "Groceries Wallet")
	#~ fuel = h5file.create_table(wallets, 'fuel',_table, "Fuel Wallet")
	#~ alcohol = h5file.create_table(wallets, 'alcohol',_table, "Alcohol Wallet")
	#~ retail = h5file.create_table(wallets, 'retail',_table, "Retail Wallet")
	#~ houseBills = h5file.create_table(wallets, 'houseBills',_table, "House Bills Wallet")
	#~ unitBills = h5file.create_table(wallets, 'unitBills',_table, "Unit Bills Wallet")
	#~ houseRent = h5file.create_table(wallets, 'houseRent',_table, "House Rent Wallet")
	#~ unitRent = h5file.create_table(wallets, 'unitRent',_table, "Unit Rent Wallet")
	#~ velseis = h5file.create_table(wallets, 'velseis',_table, "Velseis Wallet")
	#~ other = h5file.create_table(wallets, 'other',_table, "Other Wallet")