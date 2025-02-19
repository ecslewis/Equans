from urllib.parse import quote_plus
import datetime
import pandas as pd
from sqlalchemy import create_engine, event

#this is a change!!

# CONNECT=mssql+pyodbc:///?odbc_connect={}".format(
#     quote_plus(
#         "DRIVER={SQL Server};SERVER=.\SQLSERVER2019;DATABASE=Countries;"
#         "Trusted_Connection=yes;"
#     )
# )
engine = create_engine(CONNECT)

file="data.csv"
@event.listens_for(engine, "before_cursor_execute")
def receive_before_cursor_execute(
    conn, cursor, statement, params, context, executemany
):
    if executemany:
        cursor.fast_executemany = True


csv_file = pd.read_csv(file)

csv_file.to_sql(file,engine, if_exsit="Append",index=False,chunksize=1000)

print("data exported to SQL server!")
