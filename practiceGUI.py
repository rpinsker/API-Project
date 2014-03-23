#!/usr/bin/python

import Tkinter
import xml.etree.ElementTree as ET
from urllib2 import urlopen
from json import load, dumps
import xml.etree.ElementTree as ET
import re
import httplib


class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        # State initialization
        self.stateEntryVariable = Tkinter.StringVar()
        self.stateBox = Tkinter.Entry(self,textvariable=self.stateEntryVariable)
        self.stateBox.grid(column=1,row=0,sticky='EW')
        #self.stateBox.bind("<Return>", self.OnButtonClick)
        self.stateEntryVariable.set(u"")

        self.statePromptVariable = Tkinter.StringVar()
        statePrompt = Tkinter.Label(self,textvariable=self.statePromptVariable, 
                                    anchor="w",fg="white",bg="blue")
        statePrompt.grid(column=0,row=0,sticky='EW')
        self.statePromptVariable.set(u"Enter two letter state abbreviation")

        #stateButton = Tkinter.Button(self,text=u"Enter",command=self.OnButtonClick)
        #stateButton.grid(column=2,row=0)

        self.stateLabelVariable = Tkinter.StringVar()
        #stateLabel = Tkinter.Label(self,textvariable=self.stateLabelVariable,
        #                      anchor="w",fg="white",bg="blue")
        #stateLabel.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.stateLabelVariable.set(u"")
        
        # City initialization
        self.cityEntryVariable = Tkinter.StringVar()
        self.cityBox = Tkinter.Entry(self,textvariable=self.cityEntryVariable)
        self.cityBox.grid(column=1,row=1,sticky='EW')
        self.cityBox.bind("<Return>", self.OnButtonClickCity)
        self.cityEntryVariable.set(u"")

        self.cityPromptVariable = Tkinter.StringVar()
        cityPrompt = Tkinter.Label(self,textvariable=self.cityPromptVariable, 
                                    anchor="w",fg="white",bg="blue")
        cityPrompt.grid(column=0,row=1,sticky='EW')
        self.cityPromptVariable.set(u"Enter city")

        cityButton = Tkinter.Button(self,text=u"Enter",command=self.OnButtonClickCity)
        cityButton.grid(column=2,row=1)

        self.cityLabelVariable = Tkinter.StringVar()
        self.cityAndStateLabelVariable = Tkinter.StringVar()
        cityLabel = Tkinter.Label(self,textvariable=self.cityAndStateLabelVariable,
                              anchor="w",fg="white",bg="blue")
        cityLabel.grid(column=0,row=3,columnspan=2,sticky='EW')
        self.cityLabelVariable.set(u"")


        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())       
        self.stateBox.focus_set()
        self.stateBox.selection_range(0, Tkinter.END)
        self.cityBox.focus_set()
        self.cityBox.selection_range(0, Tkinter.END)

    #def OnButtonClick(self):
    #    self.stateLabelVariable.set( self.stateEntryVariable.get() )
    #    self.stateBox.focus_set()
    #    self.stateBox.selection_range(0, Tkinter.END)

    def OnButtonClickCity(self):
        self.cityAndStateLabelVariable.set( "Getting weather in " + self.cityEntryVariable.get() + ", " + self.stateEntryVariable.get() + "...")
        self.cityBox.focus_set()
        self.cityBox.selection_range(0, Tkinter.END)
        self.getInfo()

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
        #print(url)

        response = urlopen(url)
        tree = ET.parse(response)
        root = tree.getroot()
        
        current_observation = root.find('current_observation')
        location_string = current_observation.find('display_location').find('full').text
        temperature_string = current_observation.find('temperature_string').text
        feelslike_string = current_observation.find('feelslike_string').text
        self.cityAndStateLabelVariable.set("Weather in " + location_string + " is " + temperature_string + ", but it feels like " + feelslike_string)
        self.cityBox.focus_set()
        self.cityBox.selection_range(0, Tkinter.END)


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Weather')
    app.mainloop()
