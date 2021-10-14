import csv
import datetime
import pytz
from pytz import country_timezones


def get_countries():
    countries = {}
    with open("countries.csv") as f:
        r = csv.reader(f)
        next(r, None)
        for country, code in r:
            countries[country] = code

    return countries

def day_to_datetime(country):
    zone = pytz.country_timezones(country)[0] # returns string
    tz = pytz.timezone(zone) # returns time zone object
    return datetime.datetime.now(tz)

def weekday_to_time(country, day):
    d = get_countries()
    try:
        for i in range(7):
            dt = day_to_datetime(d[country]) + datetime.timedelta(days=i)
            if day == dt.weekday():
                date = datetime.datetime.strftime(dt, "%Y-%m-%d")
                return date
    except KeyError:
        pass