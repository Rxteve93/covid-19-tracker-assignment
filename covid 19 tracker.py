import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

# Load the dataset
# Ensure the file path is correct
df = pd.read_csv('owid-covid-data.csv')

print("Data loaded successfully!")


print(df.head())



print(df.columns)

print(df.info())


print(df.isnull().sum())

countries_of_interest = ['Kenya', 'USA', 'India']
df_filtered = df[df['location'].isin(countries_of_interest)].copy()


df_filtered = df_filtered.dropna(subset=['date', 'total_cases'])


df_filtered['date'] = pd.to_datetime(df_filtered['date'])


numeric_cols = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'total_vaccinations']
for col in numeric_cols:
    df_filtered[col] = df_filtered[col].interpolate()


print(df_filtered.isnull().sum())
print("Data cleaning complete!")


plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=country)
plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['total_deaths'], label=country)
plt.title('Total COVID-19 Deaths Over Time')
plt.xlabel('Date')
plt.ylabel('Total Deaths')
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['new_cases'], label=country)
plt.title('Daily New COVID-19 Cases')
plt.xlabel('Date')
plt.ylabel('New Cases')
plt.legend()
plt.grid(True)
plt.show()


df_filtered['death_rate'] = df_filtered['total_deaths'] / df_filtered['total_cases']
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['death_rate'], label=country)
plt.title('COVID-19 Death Rate (Total Deaths / Total Cases)')
plt.xlabel('Date')
plt.ylabel('Death Rate')
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['total_vaccinations'], label=country)
plt.title('Total COVID-19 Vaccinations Over Time')
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.legend()
plt.grid(True)
plt.show()


total_population = {'Kenya': 55000000, 'USA': 330000000, 'India': 1380000000}
for country in countries_of_interest:
    df_filtered.loc[df_filtered['location'] == country, 'population'] = total_population[country]

df_filtered['percent_vaccinated'] = (df_filtered['total_vaccinations'] / df_filtered['population']) * 100

plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['percent_vaccinated'], label=country)
plt.title('Percentage of Population Vaccinated Over Time')
plt.xlabel('Date')
plt.ylabel('Percentage Vaccinated')
plt.legend()
plt.grid(True)
plt.show()


latest_data = df_filtered.groupby('location').last().reset_index()

fig = px.choropleth(latest_data,
                    locations='location',
                    locationmode='country names',
                    color='total_cases',
                    hover_name='location',
                    title='Total COVID-19 Cases by Country (Latest Date)',
                    color_continuous_scale='Viridis')
fig.show()




