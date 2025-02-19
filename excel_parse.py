import os
import datetime
import pandas as pd


#path
file_path = r"C:\Users\LG8223\OneDrive - EQUANS\Documents - NSP  - Progress Tracking (Equans)\Temp\file.csv"

df = pd.read_csv(file_path)
print("excel opened!")
df=df.drop(columns=['ID', 'Parent'], axis=1, errors= 'ignore')



for index, text in df['Status'].items():
    if isinstance(text,str) and '|' in text:
        place= text.rfind('|')
        df.at[index, 'Status']= text[place+1:].strip()

df.to_csv(file_path, index=False)
print("uploaded!")


#rename file to date
dest = datetime.datetime.now()
new_filename = file_path[:-4]+" " + dest.strftime("%Y-%m-%d") + ".csv"  # Format: 2025-02-18.csv
os.rename(file_path, new_filename)
print("renamed!")
