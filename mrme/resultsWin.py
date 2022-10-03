##########################################
# This file contains the results window  #
##########################################

#import from customtkinter, PIL, requests, os, json and shutil
from customtkinter import CTkToplevel, CTkLabel, CTkButton
from PIL import ImageTk, Image
from requests import get
from os.path import dirname, realpath, isdir
from os import mkdir, remove, listdir
from json import load
from shutil import copyfileobj


#create the display window class
class resultsWindow(CTkToplevel):

    #get the path where the program is running
    PATH = dirname(realpath(__file__))
    #set the index as 0
    index=0
    #data
    data = ""

    def __init__(self, *args, **kwargs):
            CTkToplevel.__init__(self, *args, **kwargs)

            #get the data
            data = self.data

            #function to update the download folder path
            def updateDownPath():
                with open(f"{self.PATH}/user.json", "r") as file:
                    user = load(file)
                self.save_path = user["download_path"]

            #function to create the img-cache if it doesn't exist
            def createCache():
                #check if the img-cache exists
                if not isdir(f"{self.PATH}/img-cache"):
                    mkdir(f"{self.PATH}/img-cache")

            #function to download a picture given its url
            def downloadImg(img_src):
                raw_data = get(img_src, stream=True)
                with open(f'{self.PATH}/img-cache/{self.phName}', 'wb') as file:
                    copyfileobj(raw_data.raw, file)
                del raw_data

            #function to empty the img-cache
            def emptyCache():
                createCache()
                for a in listdir(f"{self.PATH}/img-cache"):
                    if a ==".keep":
                        continue
                    try:
                        remove(f"{self.PATH}/img-cache/{a}")
                    except:
                        pass

            #function to show the selected image
            def showImages(i):
                #get the dictionary of index i
                photoDict = data[i]
                #get the rover, date, sol, id, url and image format
                self.roverN = photoDict["rover"].lower()
                self.date = photoDict["date"]
                sol = photoDict["sol"]
                self.id = photoDict["id"]
                url = photoDict["img_src"]
                self.fr = url[-3:]
                #create the name of the picture
                self.phName = f"{self.id}.{self.fr}"
                #check first if the image is already downloaded
                try:
                    self.ph = Image.open(f"{self.PATH}/img-cache/{self.phName}")
                    self.img =  ImageTk.PhotoImage(master=self, image=self.ph)
                #except: download the image
                except:
                    downloadImg(url)
                    self.ph = Image.open(f"{self.PATH}/img-cache/{self.phName}")
                    self.img =  ImageTk.PhotoImage(master=self, image=self.ph)
                #load the image
                imgLabel = CTkLabel(self, image=self.img, width=(self.w/18*16), height= (self.h/11*9))
                imgLabel.grid(row=1, column=1, rowspan=9, columnspan=16)
                #label for image n / len(list)
                nPh = f"{i+1} / {len(data)}"
                nPhLabel = CTkLabel(self, text = nPh, text_font=("Arial, 13"))
                nPhLabel.grid(row=0, column=8, columnspan=2, sticky="S")
                #label for id, date | sol and camera
                timeText = "ID: {id} | Date: {d} | SOL: {s} | {c}".format(id = self.id, d = self.date, s = sol, c=photoDict["camera"])
                infoLabel = CTkLabel(self, text = timeText, text_font=("Arial, 13"))
                infoLabel.grid(row=10, column=6, columnspan=6, sticky="N")

            #function to save the shown image to the Download folder
            def savePhoto():
                newName = f"{self.date}-{self.roverN[:4]}-{self.id}.{self.fr}"
                updateDownPath()
                savedPhoto = self.ph
                savedPhoto.save(f"{self.save_path}{newName}")
                messageLabel = CTkLabel(self, text = "Saved!", text_font=("Arial, 12"))
                messageLabel.grid(row=10, column=14, columnspan=2, sticky="NE")
                messageLabel.after(1500, messageLabel.grid_forget)

            #function for next button
            def nextFunction():
                if self.index != len(data)-1:
                    self.index += 1
                    showImages(self.index)
                    #set the state of the button
                    if self.index == len(data)-1:
                        nextButton.state = False
                    else:
                        nextButton.state = True

            #function for back button
            def backFunction():
                if self.index != 0:
                    self.index -= 1
                    showImages(self.index)
                    #set the state of the button
                    if self.index == 0:
                        backButton.state = False
                    else:
                        backButton.state = True


            #window settings
            self.h = self.winfo_screenheight()
            self.w = self.winfo_screenwidth()
            self.geometry(f"{self.w}x{self.h}")
            self.title("M.R.M.E. - Search Results")

            #set up the grid
            for i in range(0, 18):
                self.grid_columnconfigure(i, weight=1)
            for i in range(0, 12):
                self.grid_rowconfigure(i, weight=1)

            #buttons
            nextButton = CTkButton(self, width=40,height=40,corner_radius=6,text="❱", text_font=("Arial, 20"), command=nextFunction)
            backButton = CTkButton(self, width=40,height=40,corner_radius=6,text="❰", text_font=("Arial, 20"),command=backFunction)
            saveButton = CTkButton(self, width=120,height=35,corner_radius=6,text="SAVE", text_font=("Arial, 18"),command=savePhoto)

            #add all the widgets to the grid
            nextButton.grid(row=5, column=17, sticky="W")
            backButton.grid(row=5, column=0, sticky="E")
            saveButton.grid(row=10, column=16, sticky="NW")

            #set state of buttons
            if len(data) == 1:
                nextButton.state = False
            backButton.state = False

            #empty the img-cache
            emptyCache()

            #show the first image
            showImages(0)