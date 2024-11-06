import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set_style("dark")

def create_daily_rental(df):
    daily_rental_df = df.groupby('dteday')['cnt'].sum().reset_index()
    return daily_rental_df

def create_seasonal_rental(df):
    seasonal_rental = df.groupby('season')['cnt'].sum().reset_index()
    return seasonal_rental

def create_weekday_rental(df):
    weekday_rental = df.groupby('weekday')['cnt'].sum().reset_index()
    return weekday_rental

def create_weather_rental(df):
    weather_rental = df.groupby('weathersit')['cnt'].sum().reset_index()
    return weather_rental

def create_monthly_rental(df):
    monthly_rental = df.groupby('mnth')['cnt'].sum().reset_index()
    return monthly_rental

def create_temp_rental(df):
    df['temp_category'] = pd.cut(df['temp'], bins=[0, 0.2, 0.4, 0.6, 0.8, 1], labels=['Very Cold', 'Cold', 'Moderate', 'Warm', 'Hot'])
    temp_rental = df.groupby('temp_category')['cnt'].sum().reset_index()
    return temp_rental

def create_user_type_rental(df):
    user_type_rental = df.groupby('casual').agg({'cnt': 'sum', 'registered': 'sum'}).reset_index()
    return user_type_rental

def create_day_weather(df):
    df.describe(include="all")
    day_weather = df.groupby('dteday').agg({'cnt': 'mean', 'weathersit': 'mean', 'temp': 'mean', 'atemp': 'mean', 'windspeed': 'mean'}).reset_index()
    return day_weather

def create_avg_by_workingday(df):
    avg_by_workingday = df.groupby('workingday')['cnt'].mean().reset_index()
    return avg_by_workingday

def create_avg_by_holiday(df):
    avg_by_holiday = df.groupby('holiday')['cnt'].mean().reset_index()
    return avg_by_holiday

def create_combined_avg(df):
    avg_by_workingday = create_avg_by_workingday(df)
    avg_by_holiday = create_avg_by_holiday(df)

    combined_avg = pd.DataFrame({
        'Type': ['Hari Kerja', 'Bukan Hari Kerja', 'Hari Libur', 'Bukan Hari Libur'],
        'Average_Cnt': [
            avg_by_workingday.loc[1, 'cnt'], 
            avg_by_workingday.loc[0, 'cnt'], 
            avg_by_holiday.loc[1, 'cnt'],     
            avg_by_holiday.loc[0, 'cnt']   
        ]
    })
    return combined_avg

all_df = pd.read_csv("dashboard/main_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    st.image("dashboard/bike.jpg")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

daily_rental_df = create_daily_rental(main_df)
seasonal_rental = create_seasonal_rental(main_df)
weekday_rental = create_weekday_rental(main_df)
weather_rental = create_weather_rental(main_df)
monthly_rental = create_monthly_rental(main_df)
temp_rental = create_temp_rental(main_df)
user_type_rental = create_user_type_rental(main_df)
day_weather = create_day_weather(main_df)
avg_by_workingday = create_avg_by_workingday(main_df)
avg_by_holiday = create_avg_by_holiday(main_df)
combined_avg = create_combined_avg(main_df)

st.header('Bike Sharing Dashboard 🚲')

st.subheader('Daily Orders')

col1, col2 = st.columns(2)
with col1:
    total_orders = daily_rental_df['cnt'].sum()
    st.metric("Total Orders", value=total_orders)

with col2:
    total_revenue = format_currency(daily_rental_df['cnt'].sum() * 1.5, "AUD", locale='es_CO')
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rental_df["dteday"],
    daily_rental_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_title('Daily Orders', fontsize=20)
ax.set_xlabel('Date', fontsize=15)
ax.set_ylabel('Order Count', fontsize=15)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=10)
st.pyplot(fig)

st.subheader('Seasonal Rentals')
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='season', y='cnt', data=seasonal_rental, ax=ax, palette='Blues_d')
ax.set_title('Rentals by Season')
ax.set_xlabel('Season')
ax.set_ylabel('Order Count')
st.pyplot(fig)

st.subheader('Weekday Rentals')
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='weekday', y='cnt', data=weekday_rental, ax=ax, palette='Greens_d')
ax.set_title('Rentals by Weekday')
ax.set_xlabel('Weekday')
ax.set_ylabel('Order Count')
st.pyplot(fig)

st.subheader('Weather Rentals')
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='weathersit', y='cnt', data=weather_rental, ax=ax, palette='Purples_d')
ax.set_title('Rentals by Weather Situation')
ax.set_xlabel('Weather')
ax.set_ylabel('Order Count')
st.pyplot(fig)

st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='mnth', y='cnt', data=monthly_rental, ax=ax, palette='Oranges_d')
ax.set_title('Rentals by Month')
ax.set_xlabel('Month')
ax.set_ylabel('Order Count')
st.pyplot(fig)

st.subheader('Temperature Rentals')
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='temp_category', y='cnt', data=temp_rental, ax=ax, palette='coolwarm')
ax.set_title('Rentals by Temperature Category')
ax.set_xlabel('Temperature Category')
ax.set_ylabel('Order Count')
st.pyplot(fig)

st.subheader('User Type Rentals')
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='casual', y='cnt', data=user_type_rental, ax=ax, color='salmon')
sns.barplot(x='registered', y='cnt', data=user_type_rental, ax=ax, color='skyblue')
ax.set_title('Rentals by User Type')
ax.set_xlabel('User Type')
ax.set_ylabel('Order Count')
st.pyplot(fig)

st.subheader('Faktor yang Mempengaruhi terhadap Jumlah Sepeda yang Disewa')
correlations = day_weather[['cnt', 'weathersit', 'temp', 'atemp', 'windspeed']].corr()['cnt'].drop('cnt')
sorted_correlations = correlations.abs().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=sorted_correlations.index, y=sorted_correlations.values, palette='coolwarm', ax=ax)
ax.set_xlabel("Variabel")
ax.set_ylabel("Nilai Absolut Korelasi")
ax.set_xticklabels(sorted_correlations.index, rotation=45)
st.pyplot(fig)

st.subheader('Perbandingan Rata-rata Jumlah Sepeda yang Disewa: Hari Kerja vs Hari Libur')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=combined_avg, x='Type', y='Average_Cnt', palette='Set2', ax=ax)
ax.set_xlabel("Tipe")
ax.set_ylabel("Rata-rata Jumlah Sepeda yang Disewa")
ax.set_xticklabels(combined_avg['Type'], rotation=15)
st.pyplot(fig) 

st.caption('Copyright (c) Bike Sharing 2024')