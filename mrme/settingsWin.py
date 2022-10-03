###########################################
# This file contains the settings window  #
###########################################

#imports from other files
from functions import checkKey

#import from customtkinter, json, webbrowser, os
from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton
from json import load, dump
from webbrowser import open_new
from os.path import isdir, dirname

#create the settings window class
class settingsWindow(CTkToplevel):
    #path to file
    p = dirname(__file__)
    #flags for missing data in user.json
    keyMissingFlag = True
    pathMissingFlag = True

    def __init__(self, *args, **kwargs):
            CTkToplevel.__init__(self, *args, **kwargs)

            #check for missing values in user.json
            def checkMissing():
                with open(f"{self.p}/user.json", "r") as file:
                    user = load(file)
                if user["api_key"] == "":
                    self.keyMissingFlag = True
                else:
                    self.keyMissingFlag = False
                if user["download_path"] == "":
                    self.pathMissingFlag = True
                else:
                    self.pathMissingFlag = False

            #function called when the button "done" is pressed
            def apiDoneAction():
                #get the response
                api_key = keyEntry.get()
                #check if it's valid
                if checkKey(api_key):
                    with open(f"{self.p}/user.json", "r") as file:
                        user = load(file)
                    user["api_key"] = api_key
                    with open(f"{self.p}/user.json", "w") as file:
                                dump(user, file)
                    messageLabel = CTkLabel(self, text = "API key updated!", text_font=("Arial, 12"))
                    messageLabel.grid(row=5, column=1, sticky="N")
                    messageLabel.after(2500, messageLabel.grid_forget)
                else:
                    wrongApiKeyText = "ERROR: api key not valid."
                    messageLabel = CTkLabel(self, text = wrongApiKeyText, text_font=("Arial, 12"))
                    messageLabel.grid(row=5, column=1, sticky="N")
                    messageLabel.after(2500, messageLabel.grid_forget)

            #function called when download path button is pressed
            def pathDoneAction():
                #get the response
                path = pathEntry.get()
                #check if it's valid
                if isdir(path):
                    with open(f"{self.p}/user.json", "r") as file:
                        user = load(file)
                    user["download_path"] = path
                    with open(f"{self.p}/user.json", "w") as file:
                                dump(user, file)
                    messageLabel = CTkLabel(self, text = "Path updated!", text_font=("Arial, 12"))
                    messageLabel.grid(row=8, column=1, sticky="N")
                    messageLabel.after(5000, messageLabel.grid_forget)
                else:
                    wrongFolderText = "ERROR: folder not valid"
                    messageLabel = CTkLabel(self, text = wrongFolderText, text_font=("Arial, 12"))
                    messageLabel.grid(row=8, column=1, sticky="N")
                    messageLabel.after(5000, messageLabel.grid_forget)

            #function to open NASA api page
            def openSite():
                open_new("https://api.nasa.gov/")


            #window settings
            self.geometry("530x365")
            self.title("MRME - Settings")

            #labels
            welcomeText = """Welcome to the Mars Rover Media Explorer!
Are you ready to explore thousands
of pictures taken by NASA Mars Rovers?
To get started you need a NASA API key obtainable at:"""""
            welcomeLabel = CTkLabel(self, text=welcomeText, text_font=("Arial, 13"))
            apiKeyLabel = CTkLabel(self, text = "API key:", text_font=("Arial, 13"))
            downloadPathLabel = CTkLabel(self, text = "Saved images location:", text_font=("Arial, 13"))
            emptyRow1 = CTkLabel(self, text="")
            emptyRow2 = CTkLabel(self, text="")
            emptyRow3 = CTkLabel(self, text="")

            #entries
            keyEntry = CTkEntry(self, placeholder_text="Type here your API key",width=200,height=30,border_width=2,corner_radius=10)
            pathEntry = CTkEntry(self, placeholder_text="/path/to/folder",width=200,height=30,border_width=2,corner_radius=10)

            #buttons
            siteButton = CTkButton(self, width=80,height=20,corner_radius=4,text="api.nasa.gov",command=openSite)
            apiKeyButton = CTkButton(self, width=80,height=30,corner_radius=8,text="SAVE",command=apiDoneAction)
            pathButton = CTkButton(self, width=80,height=30,corner_radius=8,text="SAVE",command=pathDoneAction)

            #add them to the grid
            welcomeLabel.grid(row=0, column=0, columnspan=3, padx=20, pady=10)
            siteButton.grid(row=1, column=0, columnspan=3, sticky="N")
            apiKeyLabel.grid(row=3, column=1)
            keyEntry.grid(row=4, column=1, sticky="N")
            apiKeyButton.grid(row=4, column=2, sticky="W")
            downloadPathLabel.grid(row=6, column=1)
            pathEntry.grid(row=7, column=1, sticky="N")
            pathButton.grid(row=7, column=2, sticky="W")
            emptyRow1.grid(row=2, column=1)
            emptyRow2.grid(row=5, column=1, pady=7)
            emptyRow3.grid(row=8, column=1, pady=7)

            #highlight the field in which the data is missing
            checkMissing()
            if self.keyMissingFlag:
                messageLabel = CTkLabel(self, text = "API KEY IS MISSING!", text_font=("Arial, 12"))
                messageLabel.grid(row=5, column=1, sticky="N")
                messageLabel.after(2500, messageLabel.grid_forget)
            if self.pathMissingFlag:
                messageLabel = CTkLabel(self, text = "PATH IS MISSING!", text_font=("Arial, 12"))
                messageLabel.grid(row=8, column=1, sticky="N")
                messageLabel.after(2500, messageLabel.grid_forget)
