import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# create_season_data() bertanggung jawab untuk menyiapkan season_data.
def create_season_data(df):
    season_data = all_df[(all_df['yr_x'] == 0) | (all_df['yr_x'] == 1)].groupby(['yr_x', 'season_x'])['cnt_x'].mean().reset_index()
    return season_data

# create_weather_data() bertanggung jawab untuk menyiapkan weather_data.
def create_weather_data(df):
    weather_data = all_df.groupby('weathersit_x')['cnt_x'].sum().reset_index()
    return weather_data

# create_yearly_monthly_data() bertanggung jawab untuk menyiapkan yearly_monthly_data.
def create_yearly_monthly_data(df):
    yearly_monthly_data = all_df.groupby(['yr_x', 'mnth_x'])['cnt_x'].sum().unstack()
    return yearly_monthly_data

# create_day_type_data() bertanggung jawab untuk menyiapkan day_type_data.
def create_day_type_data(df):
    day_type_data = all_df.groupby('workingday_x')['cnt_x'].mean().reset_index()
    return day_type_data

# create_weekday_data() bertanggung jawab untuk menyiapkan weekday_data.
def create_weekday_data(df):
    weekday_data = all_df.groupby('weekday_x')['cnt_x'].mean().reset_index()
    return weekday_data

all_df = pd.read_csv("all_data2.csv")

# Seperti yang telah kita lihat pada materi Latihan Exploratory Data Analysis, all_df memiliki kolom yang bertipe datetime, yaitu dteday_x. Kolom dteday inilah yang akan menjadi kunci dalam pembuatan filter. Untuk mendukung hal ini, kita perlu mengurutkan DataFrame berdasarkan dteday_x serta memastikan kolom tersebut bertipe datetime. Berikut kode yang dapat digunakan untuk melakukan hal tersebut.
datetime_columns = ["dteday_x"]
all_df.sort_values(by="dteday_x", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday_x"].min()
max_date = all_df["dteday_x"].max()

with st.sidebar:
     # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
# start_date dan end_date di atas akan digunakan untuk memfilter all_df. Data yang telah difilter ini selanjutnya akan disimpan dalam main_df. Proses ini dijalankan menggunakan kode berikut.
main_df = all_df[(all_df["dteday_x"] >= str(start_date)) & 
                (all_df["dteday_x"] <= str(end_date))]

# DataFrame yang telah difilter (main_df) inilah yang digunakan untuk menghasilkan berbagai DataFrame yang dibutuhkan untuk membuat visualisasi data. Proses ini tentunya dilakukan dengan memanggil helper function yang telah kita buat sebelumnya.
season_data = create_season_data(main_df)
weather_data = create_weather_data(main_df)
yearly_monthly_data = create_yearly_monthly_data(main_df)
day_type_data = create_day_type_data(main_df)
weekday_data = create_weekday_data(main_df)

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Based On The Season')

season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
season_data['season_label'] = season_data['season_x'].map(season_labels)

plt.figure(figsize=(16, 8))
for year in [0, 1]:
    year_data = season_data[season_data['yr_x'] == year]
    plt.plot(year_data['season_label'], year_data['cnt_x'], label=f'Year {year}')

plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

st.pyplot(plt)

st.subheader("Relationship Between Weather and Bike Sharing Count")

weather_labels = ['Clear', 'Mist', 'Light Snow'] 

plt.figure(figsize=(5, 5))
plt.pie(weather_data['cnt_x'], labels=weather_labels, autopct='%1.1f%%', startangle=140)
plt.title('Relationship Between Weather and Bike Sharing Count')
plt.axis('equal') 

st.pyplot(plt)

st.subheader("Yearly dan Monthly")


plt.figure(figsize=(20, 10))

plt.subplot(1, 2, 1)
yearly_data = all_df.groupby('yr_x')['cnt_x'].sum()
yearly_data.plot(kind='bar', color= ["#D3D3D3", "#72BCD4"])
plt.title('Total Bike Sharing per Year')
plt.xticks(yearly_data.index, ['2011', '2012'])

plt.subplot(1, 2, 2)
monthly_data = all_df.groupby('mnth_x')['cnt_x'].sum()
monthly_data.plot(kind='bar', color= ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#D3D3D3", "#D3D3D3"])
plt.title('Total Bike Sharing per Month')
plt.xticks(monthly_data.index, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
st.pyplot(plt)

st.subheader("Bike Sharing Pattern Analysis")

# Mengatur label hari
day_labels = {0: 'Holiday', 1: 'Working Day'}
day_type_data['workingday_x'] = day_type_data['workingday_x'].map(day_labels)

# Mengatur label hari
weekday_labels = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
weekday_data['weekday_x'] = weekday_data['weekday_x'].map(weekday_labels)

plt.figure(figsize=(25, 6))

# Subplot 1: Perbedaan Pola Penyewaan Sepeda antara Hari Libur dan Hari Kerja
plt.subplot(131)
plt.bar(day_type_data['workingday_x'], day_type_data['cnt_x'], color='lightblue')
plt.title('Variations in Bike Sharing Patterns between Holiday and Workdays')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Subplot 2: Hari-Hari dalam Seminggu dengan Penyewaan Sepeda Lebih Tinggi
plt.subplot(132)
plt.bar(weekday_data['weekday_x'], weekday_data['cnt_x'], color='lightcoral')
plt.title('Weekdays with Higher Bike Sharing')
plt.grid(axis='y', linestyle='--', alpha=0.7)

st.pyplot(plt)

st.caption('Copyright (c) Dicoding 2023')