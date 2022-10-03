#########################################
# This file contains the functions used #
# by the other files                    #
#########################################

#import from requests, json and os
from requests import get


#function to check the validity of the api_key. It returns a boolean.
def checkKey(key):
    url ="https://api.nasa.gov/planetary/apod?api_key={k}".format(k = key)
    r = get(url).json()
    try:
        r["url"]
    except:
        return False
    return True

#function to check if the date input or sol for the search is correct as format and time. It returns a boolean.
def checkDate(date):
    if date == "latest" or date == "":
        return True
    else:
        try:
            x = int(date)
            if x >= 0:
                return True
        except:
            from datetime import datetime
            try:
                date = date.split("-")
                y = int(date[0])
                m = int(date[1])
                d = int(date[2])
                d = datetime(y, m, d)
            except:
                return False
        return True

#function to return the earliest date available for each rover.
def earliestDate(roverName):
    rn = roverName.lower()
    if rn == "perseverance":
        return "2021-02-18"
    elif rn == "opportunity":
        return "2004-01-25"
    elif rn == "spirit":
        return "2004-01-04"
    else:
        return "2012-08-06"

#function to return the list of the available camera given the rover name.
def cameraList(rover):
    rover = rover.lower()
    if rover == "curiosity":
        return ["all", "Front Hazard Avoidance Camera", "Rear Hazard Avoidance Camera", "Mast Camera", "Chemistry and Camera Complex", "Mars Hand Lens Imager", "Mars Descent Imager", "Navigation Camera"]
    elif rover == "opportunity" or rover == "spirit":
        return ["all", "Front Hazard Avoidance Camera", "Rear Hazard Avoidance Camera", "Navigation Camera", "Panoramic Camera", "Miniature Thermal Emission Spectrometer"]
    else:
        return ["all", 'Rover Up-Look Camera', 'Rover Down-Look Camera', 'Descent Stage Down-Look Camera', 'Parachute Up-Look Camera A', 'Parachute Up-Look Camera B', 'Navigation Camera - Left', 'Navigation Camera - Right', 'Mast Camera Zoom - Right', 'Mast Camera Zoom - Left', 'Front Hazard Avoidance Camera - Left', 'Front Hazard Avoidance Camera - Right', 'Rear Hazard Avoidance Camera - Left', 'Rear Hazard Avoidance Camera - Right', 'MEDA Skycam', 'SHERLOC WATSON Camera']

#function to convert the camera name into the camera code
def convertCamera(camera):
    camDict = {
            "Front Hazard Avoidance Camera":"FHAZ",
            "Rear Hazard Avoidance Camera":"RHAZ",
            "Mast Camera": "MAST",
            "Chemistry and Camera Complex":"CHEMCAM",
            "Mars Hand Lens Imager":"MAHLI",
            "Mars Descent Imager":"MARDI",
            "Navigation Camera":"NAVCAM",
            "Panoramic Camera":"PANCAM",
            "Miniature Thermal Emission Spectrometer":"MINITES",
            'Rover Up-Look Camera': 'EDL_RUCAM',
            'Rover Down-Look Camera': 'EDL_RDCAM',
            'Descent Stage Down-Look Camera': 'EDL_DDCAM',
            'Parachute Up-Look Camera A': 'EDL_PUCAM1',
            'Parachute Up-Look Camera B': 'EDL_PUCAM2',
            'Navigation Camera - Left': 'NAVCAM_LEFT',
            'Navigation Camera - Right': 'NAVCAM_RIGHT',
            'Mast Camera Zoom - Right': 'MCZ_RIGHT',
            'Mast Camera Zoom - Left': 'MCZ_LEFT',
            'Front Hazard Avoidance Camera - Left': 'FRONT_HAZCAM_LEFT_A',
            'Front Hazard Avoidance Camera - Right': 'FRONT_HAZCAM_RIGHT_A',
            'Rear Hazard Avoidance Camera - Left': 'REAR_HAZCAM_LEFT',
            'Rear Hazard Avoidance Camera - Right': 'REAR_HAZCAM_RIGHT',
            'MEDA Skycam': 'SKYCAM',
            'SHERLOC WATSON Camera':'SHERLOC_WATSON'
    }
    try:
        return camDict[camera].lower()
    except:
        return "all"

#function to return if time is sol or date (date must be first checked with checkDate)
def timeType(time):
    try:
        int(time)
        return "s"
    except:
        return "d"

#function to get the data given rover name, time and camera. It returns a json or it returns False if error occurred
def getPhotos(rover_name, time, camera, api_key):
    rover_name = rover_name.lower()
    camera = convertCamera(camera)

    #determine which url to use
    if time == "latest" or time == "":
        if camera == "all":
            url = "https://api.nasa.gov/mars-photos/api/v1/rovers/{r}/latest_photos?api_key={k}".format(r=rover_name, k=api_key)
        else:
            url = "https://api.nasa.gov/mars-photos/api/v1/rovers/{r}/latest_photos?api_key={k}&camera={c}".format(r=rover_name, k=api_key, c=camera)
    else:
        if timeType(time) == "d":
            if camera == "all":
                url = "https://api.nasa.gov/mars-photos/api/v1/rovers/{r}/photos?api_key={k}&earth_date={d}".format(r=rover_name, d=time, k=api_key)
            else:
                url = "https://api.nasa.gov/mars-photos/api/v1/rovers/{r}/photos?api_key={k}&earth_date={d}&camera={c}".format(r=rover_name, d = time, k=api_key, c=camera)
        else:
            if camera == "all":
                url = "https://api.nasa.gov/mars-photos/api/v1/rovers/{r}/photos?api_key={k}&sol={d}".format(r=rover_name, d=time, k=api_key)
            else:
                url = "https://api.nasa.gov/mars-photos/api/v1/rovers/{r}/photos?api_key={k}&sol={d}&camera={c}".format(r=rover_name, d = time, k=api_key, c=camera)

    #get the request
    try:
        data = get(url).json()
        data[list(data.keys())[0]][0]["sol"]
    except:
        data = False

    return data

#function to create a formatted dict. Pass False for no data.
def formatPhotos(photos, rName):
    data=[]
    d = photos[list(photos.keys())[0]]
    for a in d:
        id = a["id"]
        sol = a["sol"]
        src = a["img_src"]
        date = a["earth_date"]
        camera = a["camera"]["full_name"]
        tmp = {"rover":rName, "id":id, "img_src":src, "date":date, "sol":sol, "camera":camera}
        data.append(tmp)
    return data