import requests
import json
import time
from datetime import date

# Custom exceptions
class StationNameError(Exception):
    pass
class InvalidDateError(Exception):
    pass
class ServerError(Exception):
    pass

class Ticket:
    def __init__(self, date, dept, arv, seats):
        try:
            self.departure  = self.__getCode(dept.replace(' ', '_'))
            self.arrival    = self.__getCode(arv.replace(' ', '_'), self.departure)
            self.seats      = int(seats)

            cleaned_date    = self.__getDate(date)
            self.date       = cleaned_date.split('-')[0]
            self.month      = cleaned_date.split('-')[1]
            self.year       = cleaned_date.split('-')[2]

            self.requested_data = self.__get_raw_info()
        except StationNameError:
            print("No route found for given station names \nPlease check spelling mistakes")
        except InvalidDateError:
            print("Invalid Date \nPlease follow the DD-MM-YY pattern for entering date")
        except ServerError:
            print("Problem connecting to server \nCheck your internet service")
        

    # Gets raw json data from API
    def __get_raw_info(self):
        url = "https://www.esheba.cnsbd.com/v1/trains?journey_date={year}-{month}-{date}&from_station={fromS}&to_station={toS}&class=S_CHAIR&adult={seats}&child=0"

        try:
            return requests.get(url.format(year = self.year, month = self.month, date = self.date, fromS = self.departure, toS = self.arrival, seats = self.seats)).json()
        except:
            raise ServerError("Cannot connect to server")

    # Retrieves data from json and prints final information
    def get_info(self):
        try:
            data = self.requested_data
        except:
            return ["Please fix errors mentioned while creating ticket"]
            
        result_list = []
        try:
            for item in data:
                name = item['trn_name']
                price = item['fare']

                t = time.strptime(item['dpt_time'], "%H:%M")
                dTime = time.strftime("%I:%M %p", t)
                
                result_list.append(f"{str(name)} | Deperture: {str(dTime)} | COST: {str(price)}")
            return result_list
        except:
            return ["We don't have information for that day!"]


    # Returns code name for the stations
    def __getCode(self, _name, _from = None):
        url_allStation = 'StationNames/StationNames.json'
        url_fStation = 'StationNames/'
        nameList = []
        
        if _from is None:
            with open(url_allStation, 'r') as jFile:
                sDATA = json.load(jFile)
                for name in sDATA:
                    nameList.append(name['stn_name'])
            jFile.close()
        else:
            with open(url_fStation + _from + '.json', 'r') as jFile:
                sDATA = json.load(jFile)
                for name in sDATA:
                    nameList.append(name['dest'])
            jFile.close()
            
        search = self.__search(nameList, _name.upper())
        if search != None:
            return sDATA[search]['stn_code']
        else:
            raise StationNameError("No Route found")


    # Returns and validates date in correct form
    def __getDate(self, date_string):
        date_sliced = list(map(int, date_string.split('-')))

        day = date_sliced[0]
        month = date_sliced[1]
        year = date_sliced[2]
        cd = str(date.today())
        currDate = list(map(int, cd.split('-')))

        if year != currDate[0] or month < currDate[1] or day > 31:
            raise InvalidDateError('Invalid Date')
        else:
            returnDate = str(day) + '-' + str(month) + '-' +str(year)
            return returnDate

    # Binary search
    def __search(self, array,value):
        first = 0
        last = len(array) - 1
        check = 0
        while first <= last:
            check = (first + last) // 2
            if array[check] == value:
                return check
            elif array[check] > value:
                last = check - 1
            elif array[check] < value:
                first = check + 1
        return None


# Diver Code
if __name__ == '__main__':

    departure       = input("From: ").strip()
    arrival         = input("To: ").strip()
    departure_date  = input("Date (DD-MM-YY): ").strip()
    seats           = input("Seats: ").strip()

    ticket = Ticket(departure_date, departure, arrival, seats)
    trains = ticket.get_info()
    for train in trains:
        print(train)