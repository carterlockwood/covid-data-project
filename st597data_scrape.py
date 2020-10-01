#ST 597 COVID Data Scraping
#Carter Lockwood, Glen Barlow, Jess Calvin, Nathan Alexander
import bs4
import pandas as pd
import requests

#--------------------------------------------------------------------
#JOHN'S HOPKINS DATA
#Consists of 3 Data Frames:
#   jh_data: has most comprehensive data at a STATE level
#   jh_case_count_by_county: contains confirmed case count by COUNTY
#   jh_deaths_by_county: contains death count by COUNTY
#--------------------------------------------------------------------

jh_base_url = 'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports_us'
r = requests.get(jh_base_url)
soup = bs4.BeautifulSoup(r.content)
jh_all_links = soup.find_all(attrs = {'class':'js-navigation-open'})
jh_csv_links = [link for link in jh_all_links if link.text.endswith('.csv')]

#DICTIONARY: jh_csv_data - key is date 'MM-DD-YYYY', value is data url for csv file
jh_csv_data = {}
for link in jh_csv_links:
    current_href = link.attrs['href']
    #change link into format that's readable by pandas
    current_href = current_href.replace('blob/', '')
    current_href= f'https://raw.githubusercontent.com{current_href}'
    #making key format 'MM-DD-YYYY'
    key = link.attrs['title'].replace('.csv', '')
    jh_csv_data[key] = current_href

#JH DATA FRAME - COMPREHENSIVE STATE DATA
''' Data Frame Containing Daily Confirmed, Deaths, Recovered, and Active Case
    Counts By STATE. Also includes Incident Rate, Number of People Tested, Mortality Rate,
    Testing Rate. Also FIPS Codes, UID, and ISO Values for each location. Data updated
    daily since 04-12-2020''' 

jh_data = pd.DataFrame()
for key, value in jh_csv_data.items():
    data = pd.read_csv(value)
    jh_data = pd.concat([jh_data, data])

#JH DATA FRAME - CONFIRMED CASES COUNTY BY COUNTY
''' Data Frame Containing Daily Confirmed Case Count by County

    Contains UID, iso2, iso3, code3, FIPS data, Lat, Long coordinates
    County Name is Column 'Admin 2' 
    State Name is 'Province_State' 
    Combined Key represents combined County Name, State Name, and National Abbrev

    Each additional column is the date starting 01-22-2020
    Each row represents a county'''

jh_case_count_by_county = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')

#JH DATA FRAME - CONFIRMED DEATHS COUNTY BY COUNTY
''' Data Frame Containing Daily Confirmed Deaths By County 
    
    Columns are similar to Case Count Data Frame except
    Population Column Gives Starting County Population Count 
    From 01-22-2020'''

jh_deaths_by_county = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')







#--------------------------------------------------------------------
#BING COVID-19 DATA
#
# bing_data: data frame containing State AND County levels of Confirmed 
# Cases, Change in Confirmed Cases, Deaths Count, Change in Deaths, 
# Recoveries, Change in Recoveries, along with lat, long, country, 
# state, county name information
#--------------------------------------------------------------------

bing_data = pd.read_csv("https://raw.githubusercontent.com/microsoft/Bing-COVID-19-Data/master/data/Bing-COVID19-Data.csv")


#--------------------------------------------------------------------
#NEW YORK TIMES COVID-19 DATA
#Consists of 7 Data Frames:
#   nyt_us_data: date, case count, death count since 01-21-2020 for entire US
#   nyt_state_data: date, state, fips, death count since 01-21-2020
#   nyt_county_data: date, county, fips, cases, deaths
#
#   Live Data has same columns as the above historic data, but is updated
#   recurringly to reflect changes in the present day and finally added 
#   to the historic data at the end of the day. Would be super useful for
#   a daily tracking dashboard or something like that
#
#   nyt_mask_use_by_county is the result of a NYT poll showing each
#   county's FIPS code and then the proportion of respondents who 
#   answered NEVER, RARELY, SOMETIMES, FREQUENTLY, or ALWAYS when
#   asked "How often do you wear a mask in public when you expect to
#   be within six feet of another person?"
#--------------------------------------------------------------------

nyt_us_data = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
nyt_state_data = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
nyt_county_data = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')

nyt_live_us_data = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us.csv')
nyt_live_state_data = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv')
nyt_live_county_data = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv')

nyt_mask_use_by_county = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/mask-use/mask-use-by-county.csv')