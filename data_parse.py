import os
import datetime
import pandas as pd


#path
file_path = 'data.csv'

df = pd.read_csv(file_path)
print("excel opened!")
df=df.drop(columns=['ID', 'Parent'], axis=1, errors= 'ignore')

#for index, text in df['Status'].items():

#STRIP BEFORE |
for index, text in df['Status'].items():
    if isinstance(text,str) and '|' in text:
        place= text.rfind('|')
        df.at[index, 'Status']= text[place+1:].strip()

print("Status cell is parsed!")

#NEW CELL AHU CREATION
for index, text in df['Space'].items():
    if isinstance(text,str):
        place= text.rfind(')')
        df.at[index, 'Space']= text[:place-5]
        df.at[index, 'AHU']= text[place+1:].strip()

#KEEP ONLY RECTANGLE
df = df[df['Subject'] == "Rectangle"]
print("stripped unrelated cells!")
df.to_csv(file_path, index=False)
print("uploaded!")


#RENAME FILE TO TODAY'S DATE
dest = datetime.datetime.now()
new_filename = file_path[:-4]+" " + dest.strftime("%Y-%m-%d") + ".csv"  # Format: 2025-02-18.csv
os.rename(file_path, new_filename)
print("renamed!")
