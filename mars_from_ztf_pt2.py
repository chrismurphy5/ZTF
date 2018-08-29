import pandas as pd
import json
import ephem 

with open('query_results1.txt', 'r') as f:
    data = json.load(f)
results = data['results']

candidates = {}
for i in results:
    candidates[i['lco_id']] = i['candidate']


df = pd.DataFrame(candidates)
df_transposed = df.T
#print df_transposed
df1 = df_transposed[['filter','ra','dec','candid','magap','magpsf','distnr','classtar', 'rb']]
print df1


ra = df1['ra'].tolist()
dec = df1['dec'].tolist()
print ra, dec
print len(ra), len(dec)


#For every candidate, find which ones will be above the horizon during our observing hours
#First set the observer location: (latitude, longitude, elevation)
etelman = ephem.Observer()
etelman.lat = '35:05.8' #Degrees
etelman.lon = '-111:32.1' #De
etelman.elevation = 500 #meters