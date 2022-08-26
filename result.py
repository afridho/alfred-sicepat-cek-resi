 #!/usr/bin/python
# encoding: utf-8
#
# Copyright (c) 2022 Ridho Zega
#
# MIT License. See http://opensource.org/licenses/MIT
#
from __future__ import division, print_function, absolute_import
import json
import sys
import requests
from importlib import reload
requests.packages.urllib3.disable_warnings()
reload(sys)

baseUrl = "https://content-main-api-production.sicepat.com/public/check-awb/"

def web_url(no_resi=None): 
    url = f"{baseUrl}{no_resi}"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'} # use user-agent to prevent from blocked
    file = requests.get(url, headers=headers, verify=False)
    return file.json()

def resi_saved():
    fileJson = f"resi_saved.json"
    f = open(fileJson)
    resi_saved = json.load(f)
    return resi_saved

def get_data_options():
    data_resi_file = resi_saved()
    dataExport = []
    if int(len(data_resi_file)) > 0:
        data_resi = [x for x in data_resi_file if x['valid']] # only valid parameter to check
        for resi in data_resi:
            data_web = web_url(resi['no_resi'])
            obj = {'data_alfred' : {'product_name' : resi['product_name'], 'valid' : resi['valid'], 'created_at' : resi['created_at']}}
            data = data_web | obj # merge two dict
            dataExport.append(data)
        # print(json.dumps(dataExport, indent=4))
    return dataExport
    
def data_dummy():
    fileJson = f"response_dummy.json"
    f = open(fileJson)
    resi_saved = json.load(f)
    return resi_saved


def settings(search=None):
    # data_options = get_data_options()
    # data_options = data_dummy()
    data_options = []
    
    # variables
    result = []
    check = False
    
    # string text
    _invalid_numbers_text = 'Resi number must be digits 🚫'
    _invalid_max_digit = ' | No More 12 digits 🚫'
    _type_digits = 'Type your resi number (12 Digits). Digits now = '
    
    if len(data_options) > 0:
        for post in data_options:

            if search is not None and (post['sicepat']['result']['waybill_number'].lower().find(search.lower()) == -1) and (post['data_alfred']['product_name'].lower().find(search.lower()) == -1):
                continue
            
            if post['sicepat']['result']['waybill_number'] == search:
                check = True
            
            if post['sicepat']['status']['code'] == 200 :
                if post['sicepat']['result']['last_status']['status'] == "DELIVERED":
                    result.append({
                        # fix this type (look else of this)
                            'title':f"{post['data_alfred']['product_name']}",
                            'subtitle':f"Delivered✅     |     {post['sicepat']['result']['last_status']['date_time']}",
                            'arg':f"{post['sicepat']['result']['waybill_number']}",
                            'valid':True,
                            })
                else:
                    result.append({
                            'title':f"{post['data_alfred']['product_name']}",
                            'subtitle':f"{post['sicepat']['result']['waybill_number']}  //  📍{post['sicepat']['result']['sender']} - {post['sicepat']['result']['sender_address']}  //  {post['sicepat']['result']['last_status']['date_time']}",
                            'arg':f"{post['sicepat']['result']['waybill_number']}",
                            'valid':True,
                            'text' : {
                                'largetype' :  f"{post['sicepat']['result']['last_status']['city']}",
                            },
                            'mods' : {
                                'cmd' : {
                                    'subtitle' : f"{post['sicepat']['result']['last_status']['city']}"
                                }
                            }
                            }),
            elif post['sicepat']['status']['code'] == 400:
                    result.append({
                                'title':f"Resi Number not found. Please check again.",
                                'valid': True,
                                })
            else:
                result.append({
                        'title': 'Error workflow',
                        'subtitle':f"Contact developer for support.",
                        'valid': True,
                        })
        
    if len(search) == 12 and len(data_options) != 0 :
        if not check:
            result.append({
                        'title': search,
                        'subtitle':f"{('⌘ Save Resi Number✅') if search.isnumeric() else _invalid_numbers_text }",
                        'valid': True if search.isnumeric() and len(search) == 12 else False,
                        'mods':{
                                'cmd' : {
                                    'subtitle' : 'Save resi number✓'
                                }
                            }
                        })
    elif len(search) > 0 and len(search) != 12 and len(data_options) != 0: 
            if len(search) > 12:
                result.append({
                        'title': search,
                        'subtitle':f"{(_type_digits + str(len(search)) if search.isnumeric() else _invalid_numbers_text)} {(_invalid_max_digit if len(search) > 12 else '')}",
                        'valid': False,
                        })
            else:       
                result.append({
                            'title': search,
                            'subtitle':f"{(_type_digits + str(len(search)) if search.isnumeric() else _invalid_numbers_text)}",
                            'valid': False,
                            })
    else:
        if len(search) == 0 and len(data_options) == 0:
            result.append({
                        'title' : f"SiCepat cek resi",
                        'subtitle':f"No saved resi number. Type your no resi and ⌘ to save.",
                        'valid': False,
                        })
        elif len(search) > 0 and len(search) != 12 and len(data_options) == 0:
            if len(search) > 12:
                result.append({
                        'title': search,
                        'subtitle':f"{(_type_digits + str(len(search)) if search.isnumeric() else _invalid_numbers_text)} {(_invalid_max_digit if len(search) > 12 else '')}",
                        'valid': False,
                        })
            else:       
                result.append({
                            'title': search,
                            'subtitle':f"{(_type_digits + str(len(search)) if search.isnumeric() else _invalid_numbers_text)}",
                            'valid': False,
                            })
        elif len(search) == 12 or len(data_options) == 0 :
            if not check:
                result.append({
                            'title': search,
                            'subtitle':f"{('⌘ Save Resi Number✅') if search.isnumeric() else _invalid_numbers_text }",
                            'valid': True if search.isnumeric() and len(search) == 12 else False,
                            'mods':{
                                'cmd' : {
                                    'subtitle' : 'Save resi number✓'
                                }
                            }
                            })
    return result


"""Run Script Filter."""
def main():
    SEARCH = sys.argv[1] if len(sys.argv) >= 2 else None
    posts  = settings(search=SEARCH)
    data = json.dumps({"items": posts }, indent=4) # make "rerun" : 0.1
    print(data)

if __name__ == '__main__':
    main()
    # get_data_options()