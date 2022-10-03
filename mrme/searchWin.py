######################################
#   This file is launched by MRME.py #
#   It contains the search window    #
######################################

#imports from other files
from functions import cameraList, checkDate, earliestDate, getPhotos, formatPhotos
from resultsWin import resultsWindow
from settingsWin import settingsWindow

#imports from customtkinter, os, json
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkOptionMenu
from os.path import dirname, realpath
from json import load


#create the search frame
class searchWindow(CTk):

    #rover and camera
    rover = "Perseverance"
    camera = "all"
    #path where the file is running
    PATH = dirname(realpath(__file__))
    #flags for missing data in user.json
    keyMissingFlag = False
    pathMissingFlag = False

    def __init__(self, *args, **kwargs):
        CTk.__init__(self, *args, **kwargs)

        #function to load the api key from user.json
        def updateKey():
            with open(f"{self.PATH}/user.json", "r") as file:
                user = load(file)
            self.api_key = user["api_key"]

        #function to check for missing values in user.json
        def checkMissing():
            with open(f"{self.PATH}/user.json", "r") as file:
                    user = load(file)
            if user["api_key"] == "":
                self.keyMissingFlag = True
            else:
                self.keyMissingFlag = False
            if user["download_path"] == "":
                self.pathMissingFlag = True
            else:
                self.pathMissingFlag = False

        #function to check the validity of input and open the results window
        def searchButtonAction():
            #check for valid values in user.json
            checkMissing()
            if not self.keyMissingFlag and not self.pathMissingFlag:
                date = dateInput.get()
                #check if the date format is correct
                if checkDate(date) == False:
                    wrongDateText = "Wrong date format!!"
                    messageLabel = CTkLabel(text = wrongDateText, text_font=("Arial, 12"))
                    messageLabel.grid(row=3, column=1, columnspan=2, sticky="N")
                    messageLabel.after(5000, messageLabel.grid_forget)
                else:
                    #get photos from api
                    updateKey()
                    d = getPhotos(self.rover, date, self.camera, self.api_key)
                    #check if d is False
                    if d == False:
                        wrongText ="""No photos found!
Try with a different date or camera.
Earliest available date:
{d}.""".format(d = earliestDate(self.rover))
                        messageLabel = CTkLabel(text = wrongText, text_font=("Arial, 12"))
                        messageLabel.grid(row=3, column=1, columnspan=2, rowspan=2, sticky="N")
                        messageLabel.after(5000, messageLabel.grid_forget)
                    else:
                        data = formatPhotos(d, self.rover)
                        #start the display class
                        resultsWindow.data = data
                        results = resultsWindow(self)
            else:
                openSettings()

        #rover choice action
        def getRoverName(choice):
            self.rover = choice
            #insert the camera dropdown list based on the rover name
            self.camera_ddList = CTkOptionMenu(values=cameraList(self.rover),height=36, width=290, corner_radius=8, dropdown_hover_color="grey", command=getCamera)
            self.camera_ddList.set("all")
            self.camera_ddList.grid(row=2, column=3, sticky="N")

        #camera choice action
        def getCamera(choice):
            self.camera = choice

        #function to open the settings
        def openSettings():
            sett = settingsWindow(self)


        #window settings
        self.geometry("960x540")
        self.title("M.R.M.E. - Search")

        #set up the grid
        for i in range(0, 4):
            self.grid_columnconfigure(i, weight=1)
        for i in range(0, 5):
            self.grid_rowconfigure(i, weight=1)

        #labels
        emptyRow = CTkLabel(self, text = "")
        roverSelectionLabel = CTkLabel(text = "Rover:", text_font=("Arial, 15"))
        dateSelectionLabel = CTkLabel(text = "Time:", text_font=("Arial, 15"))
        cameraSelectionLabel = CTkLabel(text = "Camera:", text_font=("Arial, 15"))

        #entries
        dateInput = CTkEntry(placeholder_text="YYYY-MM-DD or SOL or blank=latest", width=250, height=36,border_width=2,corner_radius=8)

        #buttons
        searchButton = CTkButton(width=180,height=50,corner_radius=11,text="SEARCH", text_font=("Arial, 18"),command=searchButtonAction)
        settingsButton = CTkButton(width=50, height=50, text="⚙️", corner_radius=15, text_font=("Arial, 25"), command=openSettings)

        #dropdown choices
        rover_ddList = CTkOptionMenu(values=["Curiosity", "Opportunity", "Spirit", "Perseverance"], height=36, width=250, corner_radius=8, dropdown_hover_color="grey", command=getRoverName)
        rover_ddList.set("Perseverance")
        camera_ddList = CTkOptionMenu(values=cameraList(self.rover),height=36, width=290, corner_radius=8, dropdown_hover_color="grey", command=getCamera)
        camera_ddList.set("all")

        #insert them all
        emptyRow.grid(row=3, column=0)
        roverSelectionLabel.grid(row=1, column=0)
        rover_ddList.grid(row=2, column=0, sticky="N")
        dateSelectionLabel.grid(row=1, column=1, columnspan=2)
        dateInput.grid(row=2, column=1, columnspan=2, sticky="N", padx=20)
        cameraSelectionLabel.grid(row=1, column=3)
        searchButton.grid(row=4, column=1, columnspan=2, sticky="N")
        settingsButton.grid(row=4, column=3, sticky="N")
        camera_ddList.grid(row=2, column=3, sticky="N")

        #open the settings window if either api_key field and download path is blank
        checkMissing()
        if self.keyMissingFlag or self.pathMissingFlag:
            openSettings()


#start the app
if __name__ == "__main__":
    app = searchWindow()
    app.mainloop()
