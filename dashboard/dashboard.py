import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from babel.numbers import format_currency
sns.set_theme(style='dark')

def get_monthly_total_df(df):
    monthly_df = df.resample(rule='MS', on='dteday').agg({
        "dteday": "first",
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return monthly_df

all_df = pd.read_csv("./main_data.csv")
datetime_columns = ["dteday"]

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])
    
min_date = "2011-01-01"
max_date = "2012-12-31"
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Date Range',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )    


main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
            (all_df["dteday"] <= str(end_date))]

monthly_df = get_monthly_total_df(main_df)

st.header('Final Project Dicoding Data Analysis')

st.subheader('Total Transaction')

col1, col2, col3 = st.columns([1,1,2])
 
with col1:
    total_orders = monthly_df.cnt.sum()
    st.metric("Total", value= "{:,.0f}".format(total_orders))
 
with col2:
    total_registerd = monthly_df.registered.sum()
    total_casual = monthly_df.casual.sum()
    
    st.metric("Total Registered", value= "{:,.0f}".format(total_registerd))
    st.metric("Total Nonregistered", value= "{:,.0f}".format(total_casual)+" ")

with col3:
    labels = ('Registered', 'Other')
    totals = (monthly_df.registered.sum(), monthly_df.casual.sum())
    colors = ('#93C572', '#FFF8DC')
    explode = (0, 0)

    fig, ax = plt.subplots()
    ax = plt.pie(
        x=totals,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors,
        explode=explode
    )
    st.pyplot(fig)

fig, ax = plt.subplots()

sns.histplot(data=monthly_df, x='dteday', weights='cnt', ax=ax, bins=15, kde=True)

ax.set_ylabel(None)
ax.set_xlabel("Date", fontsize=10)
ax.set_title("Monthly Transaction", loc="center", fontsize=18)
ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10, rotation=45)

st.pyplot(fig)