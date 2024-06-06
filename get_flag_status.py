import requests 
from bs4 import BeautifulSoup 
import json
from datetime import datetime
import os
  
def read_config(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def write_config(file_path, data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

def get_ri_flag_status():

    #get current running path
    path = os.path.dirname(os.path.realpath(__file__))

    read_cfg = read_config(path + "/ri.json")
    us_last_status = read_cfg.get('us_flag_status')
    ri_last_status = read_cfg.get('ri_flag_status')
    log = open(path + "/ri_flag_status.log", "a")

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    log.write(f"Date and Time of last run : {dt_string}\n")

    # Making a GET request 
    r = requests.get('https://governor.ri.gov/') 
    
    # Parsing the HTML 
    soup = BeautifulSoup(r.content, 'html.parser') 
    s = soup.find('div', class_='qh__paragraph') 
    content = s.find_all('p') 
    
    for test in content: 
        ftype = test.text.split(":")

        if "United States" in ftype[0]: 
            us_status = ftype[1].replace('\u00a0', '')
            log.write(f"United States Flag Status: " + us_status.replace('\u00a0', '') + "\n")
        if "Rhode Island" in ftype: 
            ri_status = ftype[1].replace('\u00a0', '')
            log.write(f"Rhode Island Flag Status: " + ri_status.replace('\u00a0', '') + "\n")
    
    if us_last_status != us_status:
        log.write(f"The Status of the US flag has changed.\n")
    
    if ri_last_status != ri_status:
        log.write(f"The Status of the RI flag has changed.\n")

    data = {
        "us_flag_status": us_status,
        "ri_flag_status": ri_status
    }
    write_config('ri.json', data)    
    log.close()

def get_ct_flag_status():

    #get current running path
    path = os.path.dirname(os.path.realpath(__file__))

    read_cfg = read_config(path + "/ct.json")
    us_last_status = read_cfg.get('us_flag_status')
    ct_last_status = read_cfg.get('ct_flag_status')

    log = open(path + "/ct_flag_status.log", "a")

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
            log.write(f"United States Flag Status: " + us_status + "\n")
        if "Connecticut Flag" in ftype: 
            ct_status = fstatus
            log.write(f"Connecticut Flag Status: " + ct_status + "\n")


    if us_last_status != us_status:
        log.write(f"The Status of the US flag has changed.\n")
    
    if ct_last_status != ct_status:
        log.write(f"The Status of the CT flag has changed.\n")

    data = {
        "us_flag_status": us_status,
        "ct_flag_status": ct_status
    }

    write_config('ct.json', data)    
    log.close()

get_ri_flag_status()
get_ct_flag_status()
