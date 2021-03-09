from datetime import datetime, timedelta
from manage_counties import checkDate
from urllib.request import urlopen
import sqlite3
import ssl

#-----------------------------------------------------------------------------#

today = datetime.today().date()
yesterday = today - timedelta(days=1)

url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'

#Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

covid_data_conn = sqlite3.connect('covid_data.sqlite')
covid_data_cur = covid_data_conn.cursor()

#-----------------------------------------------------------------------------#

# Example data:
# '2020-01-21,Snohomish,Washington,53061,1,0'
# date[0], county[1], state[2], fips[3], cases[4], deaths[5]

def updateData():
# Create a list of FIPS codes/counties to search for in the data
    covid_data_cur.execute('''SELECT fips FROM counties''')
    raw_fips = covid_data_cur.fetchall()
    fips_list = [fips[0] for fips in raw_fips]
    github_conn = urlopen(url, context = ctx)
    for line in github_conn:
        line = line.rstrip().decode().split(',')
# Skip line if the date is not yesterday or the county is not being tracked
        if line[0] != str(yesterday) or line[3] not in fips_list: continue
        covid_data_cur.execute('''UPDATE counties SET date = ?, cases = ?,
        deaths = ? WHERE fips = ?''', (str(yesterday), line[4], line[5], line[3]))
    covid_data_conn.commit()

#-----------------------------------------------------------------------------#

needsUpdate = checkDate()
if needsUpdate or needsUpdate == None:
    print(f"\nToday is {today.strftime('%x')}. Updating data...\n")
    updateData()
else:
    print(f"\nToday is {today.strftime('%x')}. All data is up to date.\n")

covid_data_cur.execute('''SELECT county, cases, deaths FROM counties
ORDER BY cases DESC''')
data = covid_data_cur.fetchall()
covid_data_cur.close()
print(f"As of {yesterday.strftime('%x')}:")
for county in data:
    print(f"* {county[0]} - {county[1]:,d} cases, {county[2]:,d} deaths")
