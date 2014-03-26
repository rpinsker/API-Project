#!/usr/bin/python

import Tkinter
import xml.etree.ElementTree as ET
from urllib2 import urlopen
import base64
import xml.etree.ElementTree as ET
import re
import httplib
import time
from json import load, dumps

# This application allows the user to enter a city and a state to get the current weather for that location via the Weather Underground API. It also uses the API to get the average temperature for today's date over the past five years and then shows each year's average as well as the average of all of the averages. 

# url for Weather Underground logo: http://icons-ak.wxug.com/graphics/wu2/logo_130x80.png
# url for foursquare logo: http://www.northstarcasinoresort.com/AssetsClient/Images/Social%20Media%20Sites/foursquare-logo.gif

class simpleapp_tk(Tkinter.Tk):
    # initialize window
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    # make widgets
    def initialize(self):
        self.grid()

        # add weather underground logo
        # open the image from a url
        f = urlopen("http://upload.wikimedia.org/wikipedia/en/3/3b/Weatherunderground_logo.gif").read()
        image_b64 = base64.encodestring(f)
        img = Tkinter.PhotoImage(data=image_b64)
        # create a label to display the image
        logo = Tkinter.Label(self, image=img)
        logo.image = img
        logo.grid(column=1,row=3)


        # add foursquare logo
        # open the image from a url
        f2 = urlopen("http://www.northstarcasinoresort.com/AssetsClient/Images/Social%20Media%20Sites/foursquare-logo.gif").read()
        image_b64_2 = base64.encodestring(f2)
        img2 = Tkinter.PhotoImage(data=image_b64_2)
        # create a label to display the image
        logo2 = Tkinter.Label(self, image=img2)
        logo2.image = img2
        logo2.grid(column=1,row=4)

        # state initialization
        # make textbox to enter state
        self.stateEntryVariable = Tkinter.StringVar()
        self.stateBox = Tkinter.Entry(self,textvariable=self.stateEntryVariable)
        self.stateBox.grid(column=1,row=0,sticky='EW')
        self.stateEntryVariable.set(u"")

        # make label to prompt the user to enter state
        self.statePromptVariable = Tkinter.StringVar()
        statePrompt = Tkinter.Label(self,textvariable=self.statePromptVariable, 
                                    anchor="w",fg="black",bg="white")
        statePrompt.grid(column=0,row=0,sticky='EW')
        self.statePromptVariable.set(u"Enter two letter state abbreviation:")

        self.stateLabelVariable = Tkinter.StringVar()
        self.stateLabelVariable.set(u"")
        
        # city initialization
        # make textbox to enter city
        self.cityEntryVariable = Tkinter.StringVar()
        self.cityBox = Tkinter.Entry(self,textvariable=self.cityEntryVariable)
        self.cityBox.grid(column=1,row=1,sticky='EW')
        self.cityEntryVariable.set(u"")

        # make label to prompt the user to enter city
        self.cityPromptVariable = Tkinter.StringVar()
        cityPrompt = Tkinter.Label(self,textvariable=self.cityPromptVariable, 
                                    anchor="w",fg="black",bg="white")
        cityPrompt.grid(column=0,row=1,sticky='EW')
        self.cityPromptVariable.set(u"Enter city:")

        # make button to enter city and state to get weather information
        cityButton = Tkinter.Button(self,text=u"Enter",command=self.OnButtonClickCity)
        cityButton.grid(column=2,row=1)

        # make label to display weather information with city and state
        self.cityAndStateLabelVariable = Tkinter.StringVar()
        cityLabel = Tkinter.Label(self,textvariable=self.cityAndStateLabelVariable,
                              anchor="w",fg="black",bg="white")
        cityLabel.grid(column=0,row=3,sticky='EW')

        # make label to display restaurant information for city and state
        self.restaurantLabelVariable = Tkinter.StringVar()
        restaurantLabel = Tkinter.Label(self,textvariable=self.restaurantLabelVariable,anchor="w",fg="black",bg="white")
        restaurantLabel.grid(column=0,row=4,sticky='EW')

        # format the window and the widgets
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry("700x300")       
        self.stateBox.focus_set()
        self.stateBox.selection_range(0, Tkinter.END)
        self.cityBox.focus_set()
        self.cityBox.selection_range(0, Tkinter.END)

    # method for when button is clicked
    def OnButtonClickCity(self):
        self.cityAndStateLabelVariable.set( "Getting weather in " + self.cityEntryVariable.get() + ", " + self.stateEntryVariable.get() + "...")
        self.cityBox.focus_set()
        self.cityBox.selection_range(0, Tkinter.END)
        #self.getInfo()
        self.getRestaurants()

    def getRestaurants(self):
        client_id = 'ZVRKTGVSHSZWIOLKSXHNCYQKRY54LQMOSE0ZFEZK1S1JA30S'
        client_secret = 'IYKLSNKSX4J1B535VOASMBVLPUCQTIJLDBPTGQBU2GKU2YS1'
        url = 'https://api.foursquare.com/v2/venues/explore?client_id=' + client_id + '&client_secret=' + client_secret + '&v=' + time.strftime("%Y%m%d") + '%20%20&near=' + self.cityEntryVariable.get() + '+' + self.stateEntryVariable.get() + '&section=food&limit=3'
        url = re.sub('\ ','+',url)
        
        response = urlopen(url)
        json_obj = load(response)

        self.restaurantLabelVariable.set(self.restaurantLabelVariable.get() + "-------------------\nTop Restaurants in " + self.cityEntryVariable.get() + ", " + self.stateEntryVariable.get() + "\n")
        for g in json_obj['response']['groups']:
            for i in g['items']:
                self.restaurantLabelVariable.set(self.restaurantLabelVariable.get() + "NAME: " + i['venue']['name'] + "\nPHONE: " + i['venue']['contact']['formattedPhone'] + "\nADDRESS: " + i['venue']['location']['address'])
                for c in i['venue']['categories']:
                    self.restaurantLabelVariable.set(self.restaurantLabelVariable.get() + "\nTYPE: " + c['name'] + "\n\n")
        

    # method that uses API to get weather information
    def getInfo(self):
        url = 'http://api.wunderground.com/api/'
        key = '72a90c7f55f2153b'
        url = url + key
        url += '/conditions/q/'
        url += self.stateEntryVariable.get()
        url += '/'
        url += self.cityEntryVariable.get()
        url = re.sub('\ ','_',url)
        url += '.xml'

        # if user has entered both a city and a state
        if self.stateEntryVariable.get() != "" and self.cityEntryVariable.get() != "":
            # open the url and begin parsing the xml file
            response = urlopen(url)
            tree = ET.parse(response)
            root = tree.getroot()

            # get the current temperature and the feels-like temperature out of the xml file
            current_observation = root.find('current_observation')
            location_string = current_observation.find('display_location').find('full').text
            temperature_string = current_observation.find('temperature_string').text
            feelslike_string = current_observation.find('feelslike_string').text
            
            # display the weather information
            self.cityAndStateLabelVariable.set("Weather in " + location_string + " is " + temperature_string + ", but it feels like " + feelslike_string)
            self.cityBox.focus_set()
            self.cityBox.selection_range(0, Tkinter.END)
            
            # get average information for the current day
            self.getAverage()
        # otherwise tell user to enter both a city and state
        else:
            self.cityAndStateLabelVariable.set("Please fill out both city and state")
    
    # method to get the average temperature for this day over the past 5 years
    def getAverage(self):
        meanTemp = 0
        # get current year 
        currentYear = time.strftime("%Y")
        currentYearInt = int(currentYear)
        
        # loop through API calls for each of the past five years
        i = currentYearInt - 1
        while i > (currentYearInt - 6):
            url = 'http://api.wunderground.com/api/'
            url += '72a90c7f55f2153b'
            url += '/history_'
            url += str(i)
            url += time.strftime("%m%d")
            url += '/q/' + self.stateEntryVariable.get() + '/' + self.cityEntryVariable.get() + '.xml'
            url = re.sub('\ ','_',url)
            
            # open the url and begin parsing the xml file
            response = urlopen(url)
            tree = ET.parse(response)
            root = tree.getroot()
            
            # get the average temperature for that day in that year
            meanTempDay = root.find('history').find('dailysummary').find('summary').find('meantempi').text
            # update the sum of the average temperatures
            meanTemp += int(meanTempDay)
            i = i - 1
            # update the label to display this average temperature with the given year
            self.cityAndStateLabelVariable.set(self.cityAndStateLabelVariable.get() + "\n" + str(i) + " -- " + str(meanTempDay) + " F")

        # calculate the average temperature of the averages of the current day for the past five years
        meanTemp = meanTemp/5
        # display the average
        self.cityAndStateLabelVariable.set(self.cityAndStateLabelVariable.get() + "\nThe average temperature on this day in the past five years is: " + str(meanTemp) + " F")

# run the application
if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Local Information')
    # run forever
    app.mainloop()
