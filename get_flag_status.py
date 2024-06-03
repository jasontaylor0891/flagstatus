import requests 
from bs4 import BeautifulSoup 
import json
from datetime import datetime
  
def read_config(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def write_config(file_path, data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

read_cfg = read_config('ct.json')
last_status = read_cfg.get('us_flag_status')

#open logfile for appending
log = open("ct_flag_status.log", "a")

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
log.write(f"Date and Time of last run : {dt_string}\n")

# Making a GET request 
r = requests.get('https://portal.ct.gov/flag-status') 
  
# Parsing the HTML 
soup = BeautifulSoup(r.content, 'html.parser') 

s = soup.find('ul', class_='flag-status') 
content = s.find_all('li') 
  

for test in content: 
    ftype = str(test.contents[1])
    fstatus = test.contents[2].text
    fstatus = fstatus.replace("\r\n", "")
    fstatus = fstatus.replace("\r\r\n", "")
    fstatus = fstatus.strip()
    
    if "United States Flag" in ftype: 
        us_status = fstatus
        #print(f"United States Flag Status: " + us_status)
        #write to log file
        log.write(f"United States Flag Status: " + us_status + "\n")
    if "Connecticut Flag" in ftype: 
        ct_status = fstatus
        #print(f"Connecticut Flag Status: " + ct_status)
        log.write(f"Connecticut Flag Status: " + ct_status + "\n")


s = soup.find('p', class_='press-title') 
#print("Press Release: " + s.text)
log.write(f"Press Release: " + s.text + "\n")

data = {
    "press_release": s.text,
    "us_flag_status": us_status,
    "ct_flag_status": ct_status
}

if last_status != us_status:
    #print("Status has changed")
    log.write(f"The Status of the flag has changed.\n")

write_config('ct.json', data)

#close log file
log.close()
