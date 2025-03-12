import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
import streamlit as st

file_path = r"C:\Users\LG8223\OneDrive - EQUANS\Documents - NSP  - Progress Tracking (Equans)\Temp\data.csv"

df = pd.read_csv(file_path)
print("opened")

df.to_csv(file_path)
print("uploaded")
st.sidebar.header("Filter")
AHU = st.sidebar.multiselect(
    "Select your AHU", options= df["Space"].unique()
)
pulled = st.sidebar.multiselect(
    "Select the status", options= {"Pulled", "Not Pulled", "Pending"}
)

#category

category =st.sidebar.radio(
    "select category",
    options = {"no","yes"}
)
st.dataframe(df)
print("displayed")


