from flask import Flask, render_template, request
import pandas as pd
import random as rd

app = Flask(__name__)

def draw_winners(file_path, num_winners=5):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, 'WE Mar.16.2025', header=0, skiprows=5) #date of week

    
    df['Attendance WE March 06th 2025'] = df['Attendance WE March 06th 2025'].str.strip()
    df['Attendance WE March 15th 2025'] = df['Attendance WE March 15th 2025'].str.strip()
    df['Position'] = df['Position'].str.strip()
    
    full_attendance_06 = df['Attendance WE March 06th 2025'] == "FULL ATTENDANCE"
    full_attendance_15 = df['Attendance WE March 15th 2025'] == "FULL ATTENDANCE"
    not_foreman = ~df['Position'].str.contains("Foreman", case=False, na=False)

    df_filtered = df[full_attendance_06 & full_attendance_15 & not_foreman]
    #df_filtered = df[full_attendance & (df['Position'] != "Foreman")]
    #select winners
    winners = df_filtered.sample(n=num_winners)
    return winners[['Employee ID', 'First Name', 'Last Name']]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/draw', methods=['POST'])
def draw():
    file_path = 'attendance.xlsx'
    winners = draw_winners(file_path)
    return render_template('winners.html', winners=winners)

if __name__ == "__main__":
    app.run(debug=True)