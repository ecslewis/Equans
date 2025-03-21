#READ ME!!
# PLEASE PLACE ALL NORMAL FILES INTO A FOLDER CALLED 'data' UNDER "DOCUMENTS", WHICH IS WHERE THE PYTHON
# AND VSCODE IS INSTALLED --> TO MAKE SURE PLEASE CHECK THE COMMAND LINE, YOU SHOULD SEE:
# PS C:\Users\LG8223\OneDrive - EQUANS\Documents>
# PLACE Wall Rouh-In.csv IN "DOCUMENTS"
# THIS SERVES AS A DATA MANIPULATION ALGORITHM TO PARSE FOR PROGRESS TRACKING
# FOR QUESTIONS, PLEASE CONTACT ella.lewis@equans.com or elcslewis@gmail.com
# NOTE THE PROCESSING TIME MAY VARY DEPENDING ON THE SIZE OF RAW DATA.

import os
import datetime
import pandas as pd
import shutil
file_path = "Wall Rough-In.csv"
folder= 'data'

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


#RENAME FILE TO TODAY'S DATE
def rename(file_path):
    dest = datetime.datetime.now()
    new_filename = file_path[:-4]+" " + dest.strftime("%Y-%m-%d") + ".csv" #FORMAT YR MTH DAY -- FEEL FREE TO CHANGE!!
    os.rename(file_path, new_filename)
    print("File renamed...")
    destination= r"C:\Users\LG8223\OneDrive - EQUANS\Documents - NSP  - Progress Tracking (Equans)\Temp" # COPY ADDRESS PATH FOR EXPORT LOCATION HERE
    shutil.move(new_filename, destination)
    print("File moved...")

#Upload data for the rest of the files
for filename in os.listdir(folder):
    df1=pd.read_csv(filename)
    normal(df1, filename)
    print(filename+" successfully scraped...")
    rename(filename)
print("Uploaded into the data folder...")

#Wall Rough-In upload --> access under Documents-- IMPORTANT: DO NOT PLACE IT INTO ANY FOLDER.
df=pd.read_csv(file_path)
different(df,file_path)
rename(file_path)
print("uploaded! Program exiting...")