# Track Total COVID Cases and Deaths by U.S. County
My very first Python project is a simple command line application that can be used to track total cases of and deaths from COVID-19 in whichever U.S. counties that you choose. The data is pulled from [the NY Times's COVID-19 data](https://github.com/nytimes/covid-19-data).

## History 
As an introduction to programming and starting with next to no previous knowledge, I chose to take the University of Michigan's [Python for Everybody specialization on Coursera](https://www.coursera.org/specializations/python), taught by Dr. Chuck Severance. These were the courses that helped me fall in love with coding. 

This is my first Python project that I created beginning to end in March 2021, after finishing all five *Python for Everybody* courses. I know it's far from perfect, and I'm not sure if I'll come back and make updates one day, but I can't say I'm not proud of it.

## How It Works
* `main.py` displays your tracked counties and their most recent data. If any county is not up to date, it will pull the most recent data. Note that the most "current" numbers are actually the previous day's numbers, as the NY Times's numbers aren't finalized until the following day.

* `manage_counties.py` is used to add or remove counties from your list, as well as check which counties are currently being tracked.

* Once you start tracking at least one county, a file called `covid_data.sqlite` will be generated. This is where your tracked counties and their most recent data will be stored.

* `fips.sqlite` is a database containing FIPS codes, which refer to all counties in the United States. This file is what's referenced when you add a new county to your tracked list.

## Demo
Here's an example of what my tracker looks like:

![A screenshot of a command line running main.py.](https://i.imgur.com/RYoMOdY.png)

You can see that I'm currently tracking six counties where family and friends live. The counties you're tracking are listed in descending order of total number of COVID-19 cases. If a county has been updated at least twice, you will see the increase in cases/deaths the from the last time data was pulled in parentheses on the right.

![A screenshot of a command line running manage_counties.py](https://i.imgur.com/0hhNFoQ.png)

Running `manage_counties.py` provides a series of prompts that allows you to add or remove counties at any time. You can also view a list of currently tracked counties.

## Credits

* All COVID-19 data used in this project is taken from [the NY Times](https://github.com/nytimes/covid-19-data).
