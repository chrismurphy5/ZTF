# For every candidate, find which ones will be above the horizon during our observing hours
# First set the observer location: (latitude, longitude, elevation)

import pandas as pd
import json
import ephem 
from astropy.coordinates import EarthLocation,SkyCoord
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import AltAz
import numpy as np

#Today at 7 pm (ast) = 11pm UTC
#Current strategy at Etelman is to observe from ~7-11 pm
now = Time.now()
print now
now_str = str(now)
today = now_str.split(' ')[0]
today_7 = today + ' 23:00:00'
observing_time = Time(today_7)  


observing_location = EarthLocation(lat='18.3381', lon='-64.8941', height=500*u.m) 
def az_alt(time, ra, dec):
	observing_time = Time(time)  
	aa = AltAz(location=observing_location, obstime=observing_time)
	coord = SkyCoord(ra*u.deg, dec*u.deg)
	aa = coord.transform_to(aa)
	az = "{0.az}".format(aa) 
	az_deg = az.split(' ')[0]
	alt = "{0.alt}".format(aa)
	alt_deg = alt.split(' ')[0]
	return az_deg, alt_deg



now = Time.now()
print now
now_str = str(now)
today = now_str.split(' ')[0]

#Today at 7 pm (ast) = 11pm UTC
#Current strategy at Etelman is to observe from ~7-11 pm
today_7 = today + ' 23:00:00'


with open('query_results1.txt', 'r') as f:
    data = json.load(f)
results = data['results']

candidates = {}
for i in results:
    candidates[i['lco_id']] = i['candidate']


df = pd.DataFrame(candidates) #Columns and rows seem to be flipped in opposite way we want

#Transpose the table to make the table more readable
df_transposed = df.T

#Get these columns in case we need them later, NOTE: Much more columns are available than what we have rn
df1 = df_transposed[['filter','ra','dec','candid','magap','magpsf','distnr','classtar', 'rb']]



ra = df1['ra'].tolist()
dec = df1['dec'].tolist()
print ra, dec
print len(ra), len(dec)


four_hours_in_minutes = list(range(4*60)) # 0 - (4*60) consecutive numbers
time_change = four_hours_in_minutes*u.minute # let astropy know that every number represents a minut


for r, d in zip(ra, dec):
	for x in time_change:
		time = observing_time + x # add one minute
		print time , az_alt(time, r, d)
	print '\n'


'''
Accomplished this week:
	For every candidate, convert RA/DEC to alt az at Etelman
		Find az alt once a minute from 7pm to 11pm


Next steps:
	Ensure that Astropy is converting RA/DEC to AZ/Alt properly
	For every candidate, find when it will be highest in the sky
		Maybe create a plot of how the candidate rises and falls

	Also: combine mars from ztf.py with pt2 into one script
	
'''





