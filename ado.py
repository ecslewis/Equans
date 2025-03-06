import pandas as pd


file_path = 'ahu.xlsx'
file_path1= 'ADO.xlsx'
xls = pd.ExcelFile(file_path)
xls1 = pd.ExcelFile(file_path1)
df= pd.read_excel(xls)
df1= pd.read_excel(xls1)
df3 = df1[df1['Name'].str.contains(r'\bADO\b', na=False) | df1['Name'].str.contains(r'\bAUTO\b', na=False) | df1['Name'].str.contains(r'\bAUTOMATIC\b', na=False) ]
df3.to_excel(file_path1, index=False)
print("original parsed")
print("working on AHU")
df1['AHU'] = df1['Room']. apply(lambda x: df.loc[df['Room'] ==x, 'AHU'].values[0] if x in df['Room'].values else '')
df1.to_excel(file_path1, index = False)
print("successful transmisison of file")