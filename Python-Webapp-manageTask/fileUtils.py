import csv,json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize

class jsonexcelutils:
	def __init__(self, inFile,prop,jsonExcelInd):
			print("In Init")
	
	def getPropJson(self, inFile,prop):
		cwd = os.getcwd()
	#	print('This: ',cwd)
	#	for i in os.listdir(cwd):
	#		print(i)
		f = open(cwd+inFile,'r')
		data = json.load(f)
		
		# Closing file
		f.close()
		return (data[prop])

	def getPropPanda(self, inFile,prop):
		cwd = os.getcwd()
		with open(cwd+inFile) as json_data:
			#df = pd.json_normalize(json_data,prop,['Sequence','Name'])
			df = pd.json_normalize(json_data,'columns')
			print ('head:',df)
		#return (df.json_normalize(cwd,meta='['+prop+']'))


test = jsonexcelutils('\\projval.json','dataLoadingStatusOptions','json')


#print(test.getProp('\\projval.json','dataLoadingStatusOptions'))
#print(test.getProp('\\projval.json','people'))
pep=test.getPropJson('\\projval.json','columnsapp')		
for key,value in pep.items():
	print("key:", key,",", "value:", value)
	if 'Calc' in key:
		list =value.split('*')
		print(list)
		for i in list:
			print("ind:", i)

table_MN = pd.read_html('https://en.wikipedia.org/wiki/Minnesota')
print(f'Total tables: {len(table_MN)}')

table_MN = pd.read_html('https://en.wikipedia.org/wiki/Minnesota', match='Election results from statewide races')
print(f'Total tables1: {len(table_MN)}')
df = table_MN[0]
print(df.head())

#table_MN = pd.read_html('https://www.globes.co.il/portal/', match='מטבעות')
#print(f'Total tables1: {len(table_MN)}')
#df = table_MN[0]
#print(df.head())

table_MN = pd.read_html('https://www.globes.co.il/portal/')
print(f'Total tables1: {len(table_MN)}')
print(table_MN)

#test.getPropPanda('\\projval.json','columnsapp')
#print('pep1:',pep1)

#https://towardsdatascience.com/how-to-best-work-with-json-in-python-2c8989ff0390