# -*- coding: utf-8 -*-
"""
Created on Sun May 11 20:28:01 2025

@author: gusta
"""

import pandas as pd
from pypdf import PdfReader
import os
from io import StringIO

# Change the current working directory to the current folder
os.chdir('.')

# List files available in the directory
invoice = os.listdir()

# Load the table with TICKER, NAME AND CNPJ of brazilian companies
b3_companies = pd.read_csv('companies_b3.csv', sep=';')

path = os.getcwd()

# Creating a empty list to append the files
list_files = []

# Navigating through the folders and looking for pdf files
for (dirpath, dirnames, filenames) in os.walk(path):
    for filename in filenames:
        if filename.endswith((".pdf")):
            file_path = dirpath + '/' + filename
            list_files.append(file_path)

# Creating a empty list to append the values of invoices            
brokerage_raw =[]

# Extracting the invoice data from the invoices
for i in range(len(list_files)):
    
    pdf = PdfReader(list_files[i])
    
    text = pdf.pages[0].extract_text()
    
    data = pd.read_csv(StringIO(text), sep=' ')
    
    mask = data['MercadoMercado'].str.contains('^NM$|#|^ER$|^N1$|^ES$|^EJS$|^N2$|^EJ$|^EX$|^ED$', na=False)
    
    data = data[~mask].reset_index(drop=True)
    
    cond1 = data.eq("BOVESPA").any(axis=1)
    
    trade_data = data[cond1].dropna(axis = 1, how = 'all')
    
    invoice = text[text.find('Número da nota')+15:text.find('Data Pregão')-1]
    
    date = text[text.find('Data Pregão')+12:text.find('Nome do Cliente')-1]
    
    for j in range(len(trade_data)):        
        
        market = data.iloc[trade_data.index[j],0]
        
        cv = data.iloc[trade_data.index[j]+1,0]
        
        mk_type = data.iloc[trade_data.index[j]+2,0]
        
        name = data.iloc[trade_data.index[j]+3,0]
        
        if name.endswith('F'):
            name = name[:-1]
        
        qty = data.iloc[trade_data.index[j]+4,0]
        
        amount = data.iloc[trade_data.index[j]+5,0]
        
        total = data.iloc[trade_data.index[j]+6,0]
        
        vc = data.iloc[trade_data.index[j]+7,0]
        
        brokerage_raw.append([date, invoice, market, cv, mk_type, name, qty, amount, total, vc])
        
# Creating the dataframe to store the extracted values
brokerage = pd.DataFrame(brokerage_raw, columns = ['DATA', 'NOTA', 'MERCADO', 'C/V', 'TIPO MERCADO', 'TICKER', 'QTD','VALOR', 'TOTAL', 'D/C'])

# Defining the type of each column
brokerage['QTD'] = brokerage['QTD'].astype(int)

cols = ['VALOR', 'TOTAL']

brokerage[cols] = brokerage[cols].apply(lambda col:col.astype(str).str.replace('.', '', regex=False))

brokerage[['VALOR', 'TOTAL']] = brokerage[['VALOR', 'TOTAL']].replace(',', '.', regex=True).astype(float)

brokerage['DATA'] = pd.to_datetime(brokerage['DATA'], format = '%d/%m/%Y')

columns = ['QTD', 'VALOR', 'TOTAL']

# Making the sold stocks as negative values
brokerage[columns] = brokerage.apply(lambda row:row[columns] * -1 if row['C/V'] == 'V' else row[columns], axis=1)

# Grouping the stocks by ticker
summary = brokerage.groupby('TICKER', as_index=False)[['QTD', 'TOTAL']].sum()

summary['PMEDIO'] = summary['TOTAL']/summary['QTD']

summary = pd.merge(summary, b3_companies, on='TICKER', how='left')

summary['OBSERVACAO'] = summary['QTD'].astype(str) + " AÇÕES/COTAS DE " + summary['EMPRESA'].astype(str) + ', CNPJ ' + summary['CNPJ'].astype(str) + ', AO PREÇO MÉDIO DE R$ ' + round(summary['PMEDIO'],2).astype(str)

# Saving the values in a Excel File
with pd.ExcelWriter('nubank_pmedio.xlsx', engine='openpyxl') as writer:
    brokerage.to_excel(writer, sheet_name='Negociacoes', index=False)
    summary.to_excel(writer, sheet_name='PMedio', index=False)
