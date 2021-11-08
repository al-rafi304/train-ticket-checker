import json
import requests
import time

def _save():
    url = "https://www.esheba.cnsbd.com/v1/to-stations/"
    allStations = []

    with open('StationNames/StationNames.json', 'r') as jsonFile:
        stationNames = json.load(jsonFile)
    jsonFile.close()
    for item in stationNames:
        allStations.append(item['stn_code'])
    
    # print(*allStations)
    for station in allStations:
        s_data = requests.get(url + station).json() #get json from 

        with open('stationNames/' + station + '.json', 'w') as j_write:
            json.dump(s_data, j_write)
            j_write.close()
        time.sleep(1)
        j_write.close()

_save()