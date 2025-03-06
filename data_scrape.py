import pandas as pd

message = """
This serves as a quick check for installation equipment and their components.
README.md for more info!
"""
message1 = """
Select the type of board you are looking for:
    1 - Transformers
    2 - RP's
    3 - PP's
    4 - DP's & MDP's
"""

file_path = 'excel.xlsx'
xls = pd.ExcelFile(file_path)
print(message1)


try:
    choice = int(input("Your choice: "))
    board_list = ["Transformers", "RP's", "PP's", "DP's & MDP's"]
    
    if choice < 1 or choice > len(board_list):
        print("Invalid choice. Please enter a number between 1 and 4.")
        exit()

    #TRANSFORMER
    if choice == 1:
        df = pd.read_excel(xls, board_list[choice - 1], header=0, skiprows=8)  
    #REST OF PANELS
    else:
        df = pd.read_excel(xls, board_list[choice - 1], header=0, skiprows=7)  
    
except ValueError:
    print("Invalid input, please enter a numeric value.")
    exit()

#print(df.columns)
df.columns = df.iloc[0].astype(str).str.strip()
df = df[1:].reset_index(drop=True)


def filter_and_display(df, panel_column_name, columns_to_display, diff, tpe):
    while True:
        print(message)
        number = input("Enter panel number: ").strip().capitalize()

        #if != choice1
        if diff:
            number += tpe
        #print(number)

        
        df_clean = df.dropna(how='all').copy()
        #print(df_clean.columns)
        #debugger for column extraction
        if panel_column_name not in df_clean.columns:
            print(f"Error: Column '{panel_column_name}' not found in dataset.")
            return
        
        df_clean[panel_column_name] = df_clean[panel_column_name].astype(str).str.strip()

        filtered_df = df_clean[df_clean[panel_column_name].str.lower() == number.lower()]

        if not filtered_df.empty:
            print(f"\n{number.capitalize} Information:")
            for _, row in filtered_df.iterrows():
                row_clean = row[columns_to_display].dropna()
                print(row_clean.to_string())
        else:
            print("No matching panel found :(")

#Transformers
if choice == 1:
    diff = False
    columns_to_display = [
        "DESCRIPTION", "Supplier's System Status", "DATE RELEASED", 
        "DATE ON SITE", "On-Site Installed", "Located", "Notes"
    ]
    filter_and_display(df, "DESCRIPTION", columns_to_display, diff, tpe="") #identifier (description is where we would search for the keyword entered)

#PP,RP, DP, MDP
else:
    diff = True
    while True:
        print(message)
        print("""
              Type:
              I - Interior
              B - Tub
              T - Trim
              """)
        tpe = input("Your choice (Single character): ").strip().upper()
        if tpe not in ["I", "B", "T"]:
            print("Invalid choice-- Please enter I, B, or T.")
            continue

        columns_to_display = [
            "Panel Check", "Supplier's System Status", "DATE RELEASED", 
            "DATE ON SITE", "On-Site Installed", "Located", "Notes", "Modeled Dimension"
        ]
        filter_and_display(df, "Panel Check", columns_to_display, diff, tpe)
