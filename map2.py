import folium
import pandas as pd
import os
import requests
import csv
import math
from folium import IFrame
#List of all states, notice how some just say "North", that is used below to check if it is simply a state. Will make more efficent if have time
states = [
	'Alabama',
    'Alaska',
    'Arizona',
    'Arkansas',
    'California',
    'Colorado',
    'Connecticut',
    'Delaware',
    'District',
    'Florida',
    'Georgia',
    'Hawaii',
    'Idaho',
    'Illinois',
    'Indiana',
    'Iowa',
    'Kansas',
    'Kentucky',
    'Louisiana',
    'Maine',
    'Maryland',
    'Massachusetts',
    'Michigan',
    'Minnesota',
    'Mississippi',
    'Missouri',
    'Montana',
    'Nebraska',
    'Nevada',
    'New',
    'North',
    'Ohio',
    'Oklahoma',
    'Oregon',
    'Pennsylvania',
    'Rhode',
    'South',
    'Tennessee',
    'Texas',
    'Utah',
    'Vermont',
    'Virginia',
    'Washington',
    'West',
    'Wisconsin',
    'Wyoming',
]

#States that have multiple words, like "North Carolina"
states2 = [
    'Hampshire',
    'Jersey',
    'Mexico',
    'York',
    'Carolina',
    'Dakota',
    'Island',
    'Carolina',
    'Virgina',
]

#States that are just one word
statesSolo = [
    'Alabama',
    'Alaska',
    'Arizona',
    'Arkansas',
    'California',
    'Colorado',
    'Connecticut',
    'Delaware',
    'Florida',
    'Georgia',
    'Hawaii',
    'Idaho',
    'Illinois',
    'Indiana',
    'Iowa',
    'Kansas',
    'Kentucky',
    'Louisiana',
    'Maine',
    'Maryland',
    'Massachusetts',
    'Michigan',
    'Minnesota',
    'Mississippi',
    'Missouri',
    'Montana',
    'Nebraska',
    'Nevada',
    'Ohio',
    'Oklahoma',
    'Oregon',
    'Pennsylvania',
    'Tennessee',
    'Texas',
    'Utah',
    'Vermont',
    'Virginia',
    'Washington',
    'Wisconsin',
    'Wyoming',
]

#The website that contains the information needed, this is a good website because its stays the same url
url = "https://www.worldometers.info/coronavirus/country/us/"
r = requests.get(url)
with open('file.txt', 'w') as file:
    file.write(r.text)

#Variables that are used within the function to get the necesary data from the website, Yes kind of confusing but it works
isstate = 0
islong= 0
virCheck = 0
state = ''
count = 0
numberSet = []
citySet = []

#Opens the file that is download from the website, so everytime this program runs the numbers are updated.
f = open('file.txt')
for word in f.read().split():
    if(count > 50):
        break
    if(virCheck == 1 and word == 'Virginia'):
        state = state + ' ' + word
        #print(state)
        citySet.append(state)
        virCheck = 0
        state = ''
        islong = 0
        continue        
    if(word =='Of' and islong == 1):
        state = state + ' ' + word
        dc = state + ' Columbia'
        citySet.append(dc)
        #print(dc)
        state = ''
        islong = 0
        continue
    if(word in states2 and islong == 1):
        state = state + ' ' + word
        citySet.append(state)
        #print(state)
        state = ''
        islong = 0
        continue
    if(isstate == 1):
        commaRemove = word.replace('text-align:right">','')
        finalanswer = commaRemove.replace(',','')
        if(finalanswer.isdigit()):
            #print(finalanswer)
            numberSet.append(finalanswer)
            isstate = 0
            count = count + 1
            continue
        else:
            continue       
    if(word in states):
        if(word == 'West'):
            virCheck = 1
        if(word in statesSolo):
            citySet.append(word)
            #print(word)
        isstate = 1
        islong = 1
        state = word


#print(numberSet)

#Makes copy to be used later for the markers
markernumberset = numberSet.copy()
markercityset = citySet.copy()
#print(markernumberset)
#print(markercityset)
#print(citySet)           

with open ('mycsv.csv', 'w', newline= '') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(['State','Infected'])
    for i in range(51):
        numout = numberSet.pop(0)
        logint = int(numout)
        answerlog = (math.log10(logint))
        stateout = citySet.pop(0)
        thewriter.writerow([stateout,answerlog])
    

states = os.path.join('bigtest','us-states.json')
unemployement_data = os.path.join('mycsv.csv')
state_data = pd.read_csv(unemployement_data)

m = folium.Map(location = [48, -102], zoom_start =3)
b = folium.FeatureGroup(name='Log Scale')

#Creates the shading of map from data. (change to coronavirus data later)
folium.Choropleth (
    name = 'Log Scale',
    geo_data = states,
    data = state_data,
    columns= ['State', 'Infected'],
    key_on = 'feature.properties.name',
    legend_name='# of people infected by Covid-19 (log scale)',
    fill_color='OrRd',
    fill_opacity= 0.75,
    line_opacity= 0.4,
    ).add_to(m)

#Global tooltip
tooltip = 'Click for more information'
a = folium.FeatureGroup(name='Data about each State (Markers on Map)')
#Image for coronavrius picture (custom marker)

#global tooltip
tooltip = "Click for more info"
#Adding all 50 states markers that display the actual amount of cases
totalNumOfInfected = 0
for i in range (51):
    numpop = markernumberset.pop(0)
    statepop = markercityset.pop(0)
    testint1 = int(numpop)
    totalNumOfInfected = totalNumOfInfected + testint1
    testint2 = (f"{testint1: ,d}")
    numpop = str(testint2)
    print(numpop,statepop)
    if(statepop == 'Alabama'):
    #Alabama
        a.add_child(folium.Marker([32.318230,-86.902298],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Alaska'):
    #Alaska
        a.add_child(folium.Marker([66.160507,-153.369141],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Arizona'):
    #Arizona
        a.add_child(folium.Marker([34.048927,-111.093735],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Arkansas'):
    #Arkansas
        a.add_child(folium.Marker([34.799999,-92.199997],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'California'):
    #California
        a.add_child(folium.Marker([36.778259,-119.417931],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Colorado'):
    #Colorado
        a.add_child(folium.Marker([39.113014,-105.358887],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Connecticut'):
    #Connecticut
        a.add_child(folium.Marker([41.599998,-72.699997],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Delaware'):
    #Delaware
        a.add_child(folium.Marker([39.000000,-75.500000],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'District Of Columbia'):
    #District Of Columbia
        a.add_child(folium.Marker([38.900497,-77.007507],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Florida'):
    #Florida
        a.add_child(folium.Marker([27.994402,-81.760254],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Georgia'):
    #Georgia
        a.add_child(folium.Marker([33.247875,-83.441162],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Hawaii'):
    #Hawaii
        a.add_child(folium.Marker([19.741755,-155.844437],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Idaho'):
    #Idaho
        a.add_child(folium.Marker([44.068203,-114.742043],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Illinois'):
    #Illinois
        a.add_child(folium.Marker([40.000000,-89.000000],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Indiana'):
    #Indiana
        a.add_child(folium.Marker([40.273502, -86.126976],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Iowa'):
    #Iowa
        a.add_child(folium.Marker([42.032974, -93.581543],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Kansas'):
    #Kansas
        a.add_child(folium.Marker([38.500000, -98.000000],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Kentucky'):
    #Kentucky
        a.add_child(folium.Marker([37.839333, -84.270020],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Louisiana'):
    #Louisiana
        a.add_child(folium.Marker([30.391830, -92.329102],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Maine'):
    #Maine
        a.add_child(folium.Marker([45.367584, -68.972168],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Maryland'):
    #Maryland
        a.add_child(folium.Marker([39.045753, -76.641273],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Massachusetts'):
    #Massachusetts
        a.add_child(folium.Marker([42.407211, -71.382439],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Michigan'):
    #Michigan
        a.add_child(folium.Marker([44.182205, -84.506836],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Minnesota'):
    #Minnesota
        a.add_child(folium.Marker([46.392410, -94.636230],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Mississippi'):
    #Mississippi
        a.add_child(folium.Marker([33.000000, -90.000000],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Missouri'):
    #Missouri
        a.add_child(folium.Marker([38.573936, -92.603760],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Montana'):
    #Montana
        a.add_child(folium.Marker([46.965260, -109.533691],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Nebraska'):
    #Nebraska
        a.add_child(folium.Marker([41.500000, -100.000000],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Nevada'):
    #Nevada
        a.add_child(folium.Marker([39.876019, -117.224121],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Nevada'):
    #Nevada
        a.add_child(folium.Marker([44.000000, -71.500000],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'New Jersey'):
    #New Jersey
        a.add_child(folium.Marker([39.833851, -74.871826],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'New Mexico'):
    #New Mexico
        a.add_child(folium.Marker([34.307144, -106.018066],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    #New York
    if(statepop == 'New York'):
        a.add_child(folium.Marker([43.000000, -75.000000],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'North Carolina'):
    #North Carolina
        a.add_child(folium.Marker([35.782169, -78.793457],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'North Dakota'):
    #North Dakota
        a.add_child(folium.Marker([	47.650589, -100.437012],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Ohio'):
    #Ohio
        a.add_child(folium.Marker([40.367474, -82.996216],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Oklahoma'):
    #Oklahoma
        a.add_child(folium.Marker([36.084621, -96.921387],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Oregon'):
    #Oregon
        a.add_child(folium.Marker([44.000000, -120.500000],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Pennsylvania'):
    #Pennsylvania
        a.add_child(folium.Marker([41.203323, -77.194527],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Rhode Island'):
    #Rhode Island
        a.add_child(folium.Marker([41.700001, -71.500000],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'South Carolina'):
    #South Carolina
        a.add_child(folium.Marker([33.836082, -81.163727],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'South Dakota'):
    #South Dakota
        a.add_child(folium.Marker([44.500000, -100.000000],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Tennessee'):
    #Tennessee
        a.add_child(folium.Marker([35.860119, -86.660156],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Texas'):
    #Texas
        a.add_child(folium.Marker([31.000000, -100.000000],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Utah'):
    #Utah
        a.add_child(folium.Marker([39.419220, -111.950684],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Vermont'):
    #Vermont
        a.add_child(folium.Marker([44.000000, -72.699997],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Virginia'):
    #Virginia
        a.add_child(folium.Marker([37.926868, -78.024902],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Washington'):
    #Washington
        a.add_child(folium.Marker([47.751076, -120.740135],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'West Virginia'):
    #West Virginia
        a.add_child(folium.Marker([39.000000, -80.500000],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Wisconsin'):
    #Wisconsin
        a.add_child(folium.Marker([44.500000, -89.500000],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

    if(statepop == 'Wyoming'):
    #Wyoming
        a.add_child(folium.Marker([43.075970, -107.290283],popup='Infected: ' + numpop,tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(m)

#print(totalNumOfInfected)
testint3 = (f"{totalNumOfInfected: ,d}")
totalNumOfInfected = str(testint3)

c = folium.FeatureGroup(name='Other information about Covid-19 in the USA')

text = 'Total number of infected in the USA: ' + totalNumOfInfected
iframe = folium.IFrame(text,width=300, height=60)
popup= folium.Popup(iframe, max_width=300)
Text = folium.Marker(location= [32.953368, -70.533021],popup=popup,icon = folium.Icon(icon_color='green'))
c.add_child(Text).add_to(m)

folium.LayerControl().add_to(m)
m.save('Covid-19 map.html')
print('Map created, Now open in browser!')