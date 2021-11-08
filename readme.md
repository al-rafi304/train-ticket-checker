# A script that shows Bangladesh Railway ticket information

## Step:
1. Install all the dependencies by running this command 'pip install -r requirements.txt'
2. Run 'CheckTicket.py' python file and provide the necessary inputs
3. You are done ! The script should now show you name of the train, departure time and price
4. (Optional) SaveStations.py downloads all the necessary files (except StationName.json) that are needed to run the programm. If any files are missing or script is showing error please run this script first and wait till it stops. Then run 'CheckTicket.py'

### How it works:
Instantiating the class with required arguments retrieves data from the API and stores it in json formate. 
get_info() method formats and prints it in a nice way.