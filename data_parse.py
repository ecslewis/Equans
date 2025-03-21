#READ ME!!
# PLEASE PLACE ALL NORMAL FILES INTO A FOLDER CALLED 'data' UNDER "DOCUMENTS", WHICH IS WHERE THE PYTHON
# AND VSCODE IS INSTALLED --> TO MAKE SURE PLEASE CHECK THE COMMAND LINE, YOU SHOULD SEE:
# PS C:\Users\LG8223\OneDrive - EQUANS\Documents> or wherever you place your python file
# Note this is for compiling the python file. The excel file does not need to be in the same folder or pathway, 
# If not, please precise the full address of the excel file under the variable file_path
# PLACE Wall Rouh-In.csv IN "DOCUMENTS"
# THIS SERVES AS A DATA MANIPULATION ALGORITHM TO PARSE FOR PROGRESS TRACKING
# FOR QUESTIONS, PLEASE CONTACT ella.lewis@equans.com or elcslewis@gmail.com
#  THE PROCESSING TIME MAY VARY DEPENDING ON THE SIZE OF  DATA.

import os
import datetime
import pandas as pd
import shutil
import re
file_path = "llc.csv"

#function definition
###############1################## Normal data manipulation
def normal(df, file_path):
    print("excel opened!")
    #delete column
    df=df.drop(columns=['ID', 'Parent'], axis=1, errors= 'ignore')


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
    df['Level W']= df['Space'].str[6:9]
    df['WBS']= df['Space'].str[6:]
    df['Level A']= df['AHU'].str[:3]


    print("stripped unrelated cells!")
    df.to_csv(file_path, index=False)

###############2################## Wall Rough-In data manipulation
def different(df, file_path):
    print("excel opened...")
    #delete column
    df=df.drop(columns=['ID', 'Parent',], axis=1, errors= 'ignore')
    for index, text in df['Space'].items():
        if isinstance(text,str):
            place= text.rfind(')')
            df.at[index, 'Space']= text[:place-4]
            df.at[index, 'AHU']= text[place+1:].strip()
    
    df['Level W']= df['Space'].str[5:8]
    df['WBS']= df['Space'].str[5:].apply(lambda x: x.rstrip('-') if isinstance(x, str) else x)

    df['Level A']= df['AHU'].str[:3]
    df['Level A'] = df['Level A'].str.replace("-", "", regex=False)
    df['Level W'] = df['Level W'].str.replace("-", "", regex=False)
    df['Space'] = df['Space'].apply(lambda x: x.rstrip('-') if isinstance(x, str) else x)

    df['Status'] = df['Status'].str.replace("|Room with Constraints", "", regex=False)
    df['Status'] = df['Status'].apply(lambda x: x[x.rfind('|') + 1:].strip() if isinstance(x, str) and '|' in x else x)
    df = df[df['Subject'].isin(["Rectangle", "Polygon"])]
    print("Uploading changes to file...")
    df.to_csv(file_path, index=False)

def high(df, file_path):
    print(file_path, "opened")
    df=df.drop(columns=['ID', 'Parent',], axis=1, errors= 'ignore')
    print("columsn dropped")
    for index, text in df['Space'].items():
        if isinstance(text,str):
            place= text.rfind(')')
            df.at[index, 'WBS']= text[place+1:].strip()
            place2= text.rfind('(')
            df.at[index, 'Pour']= text[:place2-1]
    print("new columns created")
    df['Pour'] = df['Pour'].str.replace("(Pour)", "", regex=False)
    print("filter1")
    df['WBS'] = df['WBS'].str.replace("(WBS)", "", regex=False)
    df=df.drop(['Space'], axis=1, errors='ignore')
    df['Pour']= df['Pour'].str.strip()
    print("filter2")
    print("Uploading changes to file...")
    df.to_csv(file_path, index=False)


def llc(df, file_path):
    df=df.drop(columns=['ID', 'Parent'], axis=1, errors= 'ignore')
    print("columsn dropped")
    df['Status'] = df['Status'].str.replace("|Room with Constraints", "", regex=False)
    df['Status'] = df['Status'].str.replace("|Internal", "", regex=False)
    df['Status'] = df['Status'].str.replace("|Ready", "", regex=False)
    for index, text in df['Space'].items():
        if isinstance(text,str):
            place= text.rfind(')')
            df.at[index, 'Space']= text[:place-5]
            df.at[index, 'AHU']= text[place+1:].strip()
    df['WBS']= df['Space'].str[5:]


    for index, text in df['Status'].items():
        if isinstance(text,str):
            place= text.rfind('|')
            if place!=-1:
                df.at[index, 'Status']= text[place:]

    for index, text in df['Status'].items():
        if isinstance(text,str):
            place1=text.find('%')
            if place!=1:
                df.at[index, 'Ready']= text[:place1+1]
    df['Ready'] = df['Ready'].str.replace("|", "", regex=False)
    for index, text in df['Status'].items():
        if isinstance(text,str):
            if '%' not in text:
                df.at[index,'Ready']=0
    for index, text in df['Status'].items():
        if isinstance(text, str) and any(word in text for word in ["Pass", "Ready"]):
            df.at[index, 'Ready'] = '100%'
    df['Ready'] = df['Ready'].str.replace("%", "", regex=False)
    
    for index, text in df['Ready'].items():
        if isinstance(text,str):
            df.at[index, 'Ready']=float(text)/100

    df['Ready'] = df['Ready'].fillna(0)
    df=df.drop("Status", axis=1, errors="ignore")
    df = df[df['Subject'].isin(["Rectangle", "Polygon"])]
    print("done")
    df.to_csv(file_path, index=False)
#RENAME FILE TO TODAY'S DATE
def rename(file_path):
    dest = datetime.datetime.now()
    new_filename = file_path[:-4]+" " + dest.strftime("%Y-%m-%d") + ".csv" #FORMAT YR MTH DAY -- FEEL FREE TO CHANGE!!
    os.rename(file_path, new_filename)
    print("File renamed...")
    destination= r"C:\Users\LG8223\OneDrive - EQUANS\Documents - NSP  - Progress Tracking (Equans)\Temp" # COPY ADDRESS PATH FOR EXPORT LOCATION HERE
    shutil.move(new_filename, destination)
    print("File moved...")


#Wall Rough-In upload --> access under Documents-- IMPORTANT: DO NOT PLACE IT INTO ANY FOLDER.
df=pd.read_csv(file_path)

llc(df,file_path)
rename(file_path)
print("uploaded! Program exiting...")