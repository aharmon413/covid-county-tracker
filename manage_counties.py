from datetime import datetime, timedelta
import sqlite3

#-----------------------------------------------------------------------------#

today = datetime.today().date()
yesterday = today - timedelta(days=1)
covid_data_conn = sqlite3.connect('covid_data.sqlite')
covid_data_cur = covid_data_conn.cursor()

def checkDate():
    # Compare yesterday's date and check if all data is up to date.
    # Note that the covid data's most recent update is always yesterday's numbers,
    # not today's, because they change frequently throughout the day
    # and aren't posted until the day has passed.
    try:
        covid_data_cur.execute('SELECT date FROM counties ORDER BY date ASC LIMIT 1')
        last_update = covid_data_cur.fetchone()[0]
        if last_update:
            last_update = datetime.strptime(last_update, '%Y-%m-%d').date()
        return last_update is None or str(yesterday) != str(last_update)
    except: return None

def addCounty(county_state):
    # Find the FIPS code associated with the county
    try:
        fips_cur.execute('''SELECT * FROM Fips
        WHERE county_state = ?''', (county_state,))
        new_county_fips = fips_cur.fetchone()[0]
    except:
        print('County not found, please try again.\n')
        return None

    covid_data_cur.execute('''CREATE TABLE IF NOT EXISTS counties
    (fips TEXT UNIQUE, county TEXT, date TEXT, latest_cases INTEGER DEFAULT 0,
     latest_deaths INTEGER DEFAULT 0, previous_cases INTEGER DEFAULT 0,
     previous_deaths INTEGER DEFAULT 0)''')

    try:
        covid_data_cur.execute('''INSERT INTO counties (fips, county)
        VALUES (?, ?)''', (new_county_fips, county_state))
        covid_data_conn.commit()
        print('County added!\n')
    except:
        print('County is already being tracked.\n')
        return None

def deleteCounty(county_state):
    try:
        covid_data_cur.execute('''SELECT fips, county FROM counties
        WHERE county = ?''', (county_state,))
        del_county_fips = covid_data_cur.fetchone()[0]
    except:
        print('County is already not being tracked.\n')
        return None

    covid_data_cur.execute('''DELETE FROM counties WHERE fips = ?''',
    (del_county_fips,))
    print('County removed!\n')

#-----------------------------------------------------------------------------#

if __name__ == '__main__':
    fips_conn = sqlite3.connect('fips.sqlite')
    fips_cur = fips_conn.cursor()

    commands = """What would you like to do?\n1 - Add a County
2 - Delete a County\n3 - View All Currently Tracked Counties\n4 - Quit"""

    needsUpdate = checkDate()
    if needsUpdate:
        print(f"\nToday is {today.strftime('%x')}. Some data needs to be updated.\n")
    elif needsUpdate == False:
        print(f"\nToday is {today.strftime('%x')}. All data is up to date.\n")
    else:
        print(f"\nToday is {today.strftime('%x')}. Unable to retrieve date of last update.\n")

    while True:
        print(commands)
        inp = input('> ')
        if inp not in ('1', '2', '3', '4'):
            print('Invalid command.\n')
            continue
        if inp == '1':
            print('\nEnter a county name and state to add. Example: Wayne, MI')
            new_county = input('> ')
            addCounty(new_county)
            continue
        elif inp == '2':
            print('\nEnter a county name and state to delete. Example: Stanislaus, CA')
            del_county = input('> ')
            deleteCounty(del_county)
            continue
        elif inp == '3':
            try:
                covid_data_cur.execute('''SELECT county FROM counties
                ORDER BY county ASC''')
            except:
                print('\nNo counties are being tracked right now.\n')
                continue
            counties = covid_data_cur.fetchall()
            print('\nThe following counties are being tracked:')
            for county in counties: print(f'* {county[0]}')
            print('')
            continue
        else:
            covid_data_cur.close()
            fips_cur.close()
            quit()

#-----------------------------------------------------------------------------#
