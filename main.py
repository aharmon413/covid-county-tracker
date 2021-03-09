from datetime import datetime, timedelta
from manage_counties import checkDate
from urllib.request import urlopen
import sqlite3
import ssl

#-----------------------------------------------------------------------------#

today = datetime.today().date()
yesterday = today - timedelta(days=1)
covid_data_conn = sqlite3.connect('covid_data.sqlite')
covid_data_cur = covid_data_conn.cursor()

url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'

#Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#-----------------------------------------------------------------------------#

# Example data:
# '2020-01-21,Snohomish,Washington,53061,1,0'
# date[0], county[1], state[2], fips[3], cases[4], deaths[5]

def getFips():
# Create a list of FIPS codes/counties to search for in the data
    try: covid_data_cur.execute('''SELECT fips FROM counties''')
    except:
        print('No counties are being tracked. Run manage_counties.py to start tracking data.')
        quit()
    raw_fips = covid_data_cur.fetchall()
    return [fips[0] for fips in raw_fips]

def updateData():
    covid_data_cur.execute('''UPDATE counties SET previous_cases = latest_cases,
    previous_deaths = latest_deaths''')
    github_conn = urlopen(url, context = ctx)
    for line in github_conn:
        line = line.rstrip().decode().split(',')
# Skip line if the date is not yesterday or the county is not being tracked
        if line[0] != str(yesterday) or line[3] not in fips_list: continue
        covid_data_cur.execute('''UPDATE counties SET date = ?, latest_cases = ?,
        latest_deaths = ? WHERE fips = ?''', (str(yesterday), line[4], line[5], line[3]))
    covid_data_conn.commit()

def displayData():
    try:
        covid_data_cur.execute('''SELECT county, latest_cases, latest_deaths,
        previous_cases, previous_deaths FROM counties ORDER BY latest_cases DESC''')
    except:
        print('No counties are being tracked. Run manage_counties.py to start tracking data.')
        quit()
    data = covid_data_cur.fetchall()
    covid_data_cur.close()
    print(f"As of {yesterday.strftime('%x')}:")
    for county in data:
        print(f"* {county[0]}:")
        print(f"\t{county[1]:,d} cases (+{county[1]-county[3]:,d} from last update)")
        print(f"\t{county[2]:,d} deaths (+{county[2]-county[4]:,d} from last update)")

#-----------------------------------------------------------------------------#

needsUpdate = checkDate()

if needsUpdate or needsUpdate == None:
    print(f"\nToday is {today.strftime('%x')}. Updating data...\n")
    fips_list = getFips()
    updateData()
else:
    print(f"\nToday is {today.strftime('%x')}. All data is up to date.\n")

displayData()
