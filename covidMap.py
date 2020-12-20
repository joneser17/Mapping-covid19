'''
    @author - Erik Jones
    This program creates a interactive map using the library folium. On the map is the current amount of cases in each state along with the total number of cases
    (The marker is located in the atlantic ocean.) Also included on the map is an choropleth map, which is currently done in log form because of the big variation 
    of cases located in the united states. Finally, this program takes in twitterSent.py which is a sentiment analysis and puts on the map the overall feeling about
    Covid-19.
'''
import folium
import pandas as pd
import os
import requests
import csv
import math
import datetime
# import twitterSent (Twitter sentiment analysis,off by default)
from folium import IFrame

print("Calculating, please wait.......")
# Sent_result = twitterSent.info()              #(Twitter sentiment analysis,off by default)


class state_info():
    def __init__(self,name,cases):
        self.state_name = name
        self.state_cases = cases

#The website that contains the information needed, this is a good website because its stays the same url
url = "https://www.worldometers.info/coronavirus/country/us/"
r = requests.get(url)
with open('data/data.txt', 'w') as file:
    file.write(r.text)

NewStates = [
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
    'Puerto',
    'Texas',
    'Utah',
    'Of',
    'Columbia',
    'Vermont',
    'Virginia',
    'Washington',
    'West',
    'Wisconsin',
    'Wyoming',
    'Hampshire',
    'Jersey',
    'Mexico',
    'York',
    'Carolina',
    'Dakota',
    'Island',
    'Rico',
    'Carolina',
    'Virgina',
]

states_list = []
seen = False
count = 0
currentState = ''
num_states = 52

# Scrapes state name and amount of cases from website.
f = open('data/data.txt')
for word in f.read().split():
    if(count >= num_states):
        break
    if(seen == False):
        hrefCheck = word[0:4]
        if (hrefCheck == 'href'):
            theString = word.find('>')
            sizeofword = len(word)
            hrefremove = word[theString + 1:sizeofword]
            newstateGet1 = hrefremove.replace('</a>','')
            if(newstateGet1 in NewStates):     
                seen = True
                currentState = newstateGet1
        else:
            if(word in NewStates):
                currentState = word
                seen = True
    else:
        word = word.replace('</a>','')
        if(word in NewStates):
            currentState = currentState + ' ' + word
        else:
            commaRemove = word.replace('text-align:right">','')
            finalanswer = commaRemove.replace(',','')
            if(finalanswer.isdigit() and finalanswer != '0'):
                the_state = state_info(currentState,finalanswer)
                states_list.append(the_state)
                count = count + 1
                seen = False
            

# Contains state name and log base 10 of cases.        
with open ('data/state_log_info.csv', 'w', newline= '') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(['State','Infected'])
    for key in states_list:
        answerlog = (math.log10(int(key.state_cases)))
        thewriter.writerow([key.state_name,answerlog])

# Creates choropleth map with log base 10 of cases.   
states = os.path.join('states_geodata','us-states.json')
infection_data = os.path.join('data/state_log_info.csv')
state_data = pd.read_csv(infection_data)

covid_map = folium.Map(location = [48, -102], zoom_start =4,min_zoom = 3)
layer_log = folium.FeatureGroup(name='Log Scale')

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
    ).add_to(covid_map)

layer_markers = folium.FeatureGroup(name='Data about each State (Markers on Map)')

# Global tooltip
tooltip = "Click for more info"

#Adding all 50 states markers that display the actual amount of cases
state_dict = {}
f = open('states_geodata/states_center.txt')
for line in f:
    items = line.split(",")
    state_dict[items[0]] = items[1],items[2]
    
total_us_cases = 0
# Places markers on the map containing the cases with the corresponding state.
for i in states_list:
    cords = state_dict.get(i.state_name)
    cases = int(i.state_cases)
    total_us_cases = total_us_cases + cases
    layer_markers.add_child(folium.Marker([cords[0],cords[1]],popup='Infected: ' + (f"{int(i.state_cases): ,d}"),tooltip=tooltip,icon=folium.Icon(icon = 'bookmark',color='green' ))).add_to(covid_map)

Layer_other = folium.FeatureGroup(name='Other information about Covid-19 in the USA')

text = 'Total number of infected in the USA: ' + str((f"{total_us_cases: ,d}"))
iframe = folium.IFrame(text,width=300, height=60)
popup= folium.Popup(iframe, max_width=300)
Text = folium.Marker(location= [32.953368, -70.533021],popup=popup,icon = folium.Icon(icon_color='green'))
Layer_other.add_child(Text).add_to(covid_map)
'''
(Twitter sentiment analysis,off by default)

emotion = Sent_result.pop('emotion')
emotion_total = Sent_result.pop(emotion)
total_tweets = Sent_result.pop('total')

#The logo icons for possitive,neutral, negative
positive_icon = folium.features.CustomIcon('images/positive.png', icon_size =(50,50))
negative_icon = folium.features.CustomIcon('images/negative.png', icon_size =(50,50))
neutral_icon  = folium.features.CustomIcon('images/neutral.png', icon_size =(50,50))


text1 = 'Total number of tweets analyzed: ' + str(total_tweets) + '<br>' + 'Overall feeling on the coronavirus: ' + str(emotion) + '<br>' + 'Total number of ' + str(emotion) + ' tweets: ' + str(emotion_total)
iframe1 = folium.IFrame(text1,width=400, height=70)
popup1= folium.Popup(iframe1, max_width=400)
if(emotion == 'neutral'):
    c.add_child(folium.Marker([37.953368, -130.533021],popup=popup1,tooltip=tooltip,icon=neutral_icon)).add_to(m)
elif(emotion == 'negative'):
    c.add_child(folium.Marker([37.953368, -130.533021],popup=popup1,tooltip=tooltip,icon=neutral_icon)).add_to(m)
elif(emotion == 'positive'):
    c.add_child(folium.Marker([37.953368, -130.533021],popup=popup1,tooltip=tooltip,icon=neutral_icon)).add_to(m)
'''

folium.LayerControl().add_to(covid_map)
date = datetime.date.today()
covid_map.save('Maps/Covid-19 map (' + str(date) + ').html')
print('Map created, Now open in browser!')