# For every candidate, find which ones will be above the horizon during our observing hours
# First set the observer location: (latitude, longitude, elevation)

import pandas as pd
import json
import ephem 
from astropy.coordinates import EarthLocation,SkyCoord
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import AltAz
import matplotlib.pyplot as plt

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
candid = df1['candid'].tolist()
print ra, dec, candid
print len(ra), len(dec), len(candid)


four_hours_in_minutes = list(range(4*60)) # 0 - (4*60) consecutive numbers
time_change = four_hours_in_minutes*u.minute # let astropy know that every number represents a minut


candidate_az_alt = {}

for i, r, d in zip(candid, ra, dec):
	az = []
	alt = []
	az_alt_dict = {}
	for x in time_change:
		time = observing_time + x # add one minute
		azimuth , altitude = az_alt(time, r, d)
		az.append(float(azimuth))
		alt.append(float(altitude))
		az_alt_dict['azimuth'] = az 
		az_alt_dict['altitude'] = alt
	print az_alt_dict
	candidate_az_alt[i] =  az_alt_dict
	print '\n'

print candidate_az_alt

for k, v in candidate_az_alt.items():
	plt.scatter(four_hours_in_minutes, v['altitude'])
	plt.title(str(k) + 'Altitude vs Time during Observation Hours')
	plt.ylabel('Altitude')
	plt.xlabel('Minutes after 7pm ' + today)
	plt.savefig(str(k) + '.png')
	plt.clf()




'''
Accomplished this week:
	For every candidate, convert RA/DEC to alt az at Etelman
		Find az alt once a minute from 7pm to 11pm
		Create a plot of how the candidate rises and falls


Next steps:
	Ensure that Astropy is converting RA/DEC to AZ/Alt properly
	For every candidate, find when it will be highest in the sky
		Show this in the candidates altitude vs time plot
		Create table: cand id , ra , dec, time of highest point, alt at highest point, az at highest point
	Also: combine mars from ztf.py with pt2 into one script
	
'''

























