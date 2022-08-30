import json
from datetime import datetime

filename = './resi_saved.json'


# time variable
time_format = "%Y-%m-%d %H:%M"
parse_time_now = datetime.now()
time_now = parse_time_now.strftime(time_format)

def addData(no_resi=None, product_name=None):
    with open(filename) as fp:
        listObj = json.load(fp)
        listObj.append({
            "no_resi": no_resi,
            "product_name": product_name,
            "valid" : True,
            "last_update" : ''
        })
    with open(filename, 'w') as json_file:
        json.dump(listObj, json_file, 
                            indent=4,  
                            separators=(',',': '))
    print('Data saved.')
    
def deleteData(no_resi=None):
    with open(filename, 'r') as f:
        my_list = json.load(f)
        for idx, obj in enumerate(my_list):
            if obj['no_resi'] == no_resi:
                my_list.pop(idx)
    with open(filename, 'w') as f:
        f.write(json.dumps(my_list, indent=4))
"""End Delete Data Function"""

"""Begin Fill last_update if status delivered"""
def fillLastUpdate(no_resi=None, date=None):
    with open(filename, 'r') as f:
        my_list = json.load(f)
        for idx, obj in enumerate(my_list):
            if obj['no_resi'] == no_resi:
                obj['last_update'] = date
    with open(filename, 'w') as f:
        f.write(json.dumps(my_list, indent=4))

"""Begin Mark Finished Data"""
def markFinishedData(no_resi=None):
    with open(filename, 'r') as f:
        my_list = json.load(f)
        for idx, obj in enumerate(my_list):
            if obj['no_resi'] == no_resi:
                obj['valid'] = False
    with open(filename, 'w') as f:
        f.write(json.dumps(my_list, indent=4))


# addData('50', 'Wew Boy')