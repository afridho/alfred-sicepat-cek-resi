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
from utils.auto_mark_finished import doCheck
from utils.crud import fillLastUpdate
requests.packages.urllib3.disable_warnings()
from utils import get_data, logo_icon
import plistlib
reload(sys)

"""Load settings"""
file_name = "info.plist"
with open(file_name, 'rb') as g:
    plist = plistlib.load(g)  
mark_finished_days = plist["variables"]["auto_mark_finished_days"]

def resi_saved():
    fileJson = f"resi_saved.json"
    f = open(fileJson)
    resi_saved = json.load(f)
    return resi_saved



def get_data_options():
    data_resi_file = resi_saved()
    
    be = doCheck()
    for auto_check_resi in data_resi_file:
        be.compare_time(auto_check_resi['no_resi'], auto_check_resi['last_update'], mark_finished_days) # (no_resi, last_update, days compare)
    
    after_resi_file = resi_saved()
    dataExport = []
    if int(len(after_resi_file)) > 0:
        data_resi = [x for x in after_resi_file if x['valid']] # only valid parameter to check
        if len(data_resi) > 0:
            for resi in data_resi:
                data_web = get_data.web_url(resi['no_resi'])
                obj = {'data_alfred' : {'product_name' : resi['product_name'], 'valid' : resi['valid'], 'last_update' : resi['last_update']}}
                data = data_web | obj # merge two dict
                dataExport.append(data)
        # print(json.dumps(dataExport, indent=4))
    return dataExport
    
def data_dummy():
    fileJson = f"response_dummy_details.json"
    f = open(fileJson)
    resi_saved = json.load(f)
    return resi_saved
            

def results(search=None):
    data_out = get_data_options()
    data_options = [x for x in data_out if x['data_alfred']['valid']]
    # data_options = data_dummy()
    # data_options = []
    
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
                    fillLastUpdate(post['sicepat']['result']['waybill_number'], post['sicepat']['result']['last_status']['date_time'])
                    result.append({
                        # fix this type (look else of this)
                            'title':f"{post['data_alfred']['product_name']}",
                            'subtitle':f"Delivered✅   //   {post['sicepat']['result']['last_status']['date_time']}",
                            'arg':f"{post['sicepat']['result']['waybill_number']}",
                            'variables' : {
                                'resi_number' :  f"{post['sicepat']['result']['waybill_number']}",
                                'logo_icon' : f"{logo_icon.get_icon(post['sicepat']['result']['partner'])}",
                            },
                            'icon':{
                                'path' : f"{logo_icon.get_icon(post['sicepat']['result']['partner'])}"
                            },
                            'valid':True,
                            'mods' : {
                                'alt' : {
                                    'subtitle' : "Mark Finished (Delivered 🛵)",
                                    'valid' : True,
                                    'variables' : {
                                        'resi_number' :  f"{post['sicepat']['result']['waybill_number']}",
                                    },
                                },
                                'ctrl' : {
                                    'subtitle' : "Remove Resi Number",
                                    'valid' : True,
                                    'variables' : {
                                        'resi_number' :  f"{post['sicepat']['result']['waybill_number']}",
                                    },
                                }
                            }
                            })
                else:
                    result.append({
                            'title':f"{post['data_alfred']['product_name']}",
                            'subtitle':f"{post['sicepat']['result']['waybill_number']}  //  📍{post['sicepat']['result']['sender']} - {post['sicepat']['result']['sender_address']}  //  {post['sicepat']['result']['last_status']['date_time']}",
                            'arg':f"{post['sicepat']['result']['waybill_number']}",
                            'valid':True,
                            'icon':{
                                'path' : f"{logo_icon.get_icon(post['sicepat']['result']['partner'])}"
                            },
                            'variables' : {
                                'resi_number' :  f"{post['sicepat']['result']['waybill_number']}",
                                'logo_icon' : f"{logo_icon.get_icon(post['sicepat']['result']['partner'])}",    
                            },
                            'text' : {
                                'largetype' :  f"{post['sicepat']['result']['last_status']['city']}",
                            },
                            'mods' : {
                                'cmd' : {
                                    'subtitle' : f"{post['sicepat']['result']['last_status']['city']}",
                                    'valid' : False,
                                },
                                'alt' : {
                                    'subtitle' : "Mark Finished (Delivered 🛵)",
                                    'arg' : '', # make value False
                                    'valid' : True,
                                    'variables' : {
                                        'resi_number' :  f"{post['sicepat']['result']['waybill_number']}",
                                    },
                                },
                                'ctrl' : {
                                    'subtitle' : "Remove Resi Number",
                                    'valid' : True,
                                    'variables' : {
                                        'resi_number' :  f"{post['sicepat']['result']['waybill_number']}",
                                    },
                                }
                            }
                            }),
            else:
                result.append({
                        'title': 'Error workflow',
                        'subtitle':f"Contact developer for support.",
                        'valid': True,
                        })
        
    if len(search) == 12 and len(data_options) != 0 :
        if not check:
            data = get_data.web_url(search)
            if data['sicepat']['status']['code'] == 400:
                result.append({
                    'title':f"Resi Number not found. Please check again.",
                    'valid': False,
                })
            else:
                result.append({
                            'title': search,
                            'subtitle':f"Receiver: {data['sicepat']['result']['receiver_name']}  //  Sender: 📍{data['sicepat']['result']['sender']}  // valid✅",
                            'valid': True if search.isnumeric() and len(search) == 12 else False,
                            'variables' : {
                                    'resi_number' :  f"{data['sicepat']['result']['waybill_number']}",
                                    'new_resi' : True,
                                },
                            'arg' : f"{data['sicepat']['result']['waybill_number']}",
                            'mods':{
                                    'cmd' : {
                                        'subtitle' : 'Save resi number✓',
                                        'variables' : {
                                            'resi_number' : search,
                                            },
                                    }
                                }
                            })
    elif len(search) > 0 and len(search) != 12 and len(data_options) != 0 and search.isnumeric(): 
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
        if search == '!':
            
            result.append({
                        'title':'Histories (All resi number)',
                        'subtitle':'',
                        'icon': {
                            'path' : 'icon.png',
                        },
                        'arg' : 'histories',
                        'valid':True
                        })
            result.append({
                        'title': 'Settings > Auto mark finished',
                        'subtitle':'',
                        'icon': {
                            'path' : 'icon.png',
                        },
                        'arg' : 'settings_auto_mark',
                        'variables': {
                            'finished_days' : f"{mark_finished_days if mark_finished_days != '0' else ''}",
                            'finished_text' : f"{'disabled🚫' if mark_finished_days == '0' else 'days'}"
                        },
                        'valid':True
                        })
            result.append({
                        'title': 'Settings > Clear caches data',
                        'subtitle':'Clear all caches data (Cache folder of this workflow)',
                        'icon': {
                            'path' : 'icon.png',
                        },
                        'arg' : 'settings_clear_cache',
                        'valid':True
                        })
        if len(search) == 0 and len(data_options) == 0 and search.isnumeric():
            result.append({
                        'title' : f"SiCepat cek resi",
                        'subtitle':f"No saved resi number. Type your no resi and ⌘ to save.",
                        'valid': False,
                        })
        elif len(search) == 0 and len(data_options) == 0:
            result.append({
                    'title' : f"Data empty 🗑️",
                    'subtitle':f"Add some resi number to check or saved. [ ! for settings ]",
                    'valid': False,
                    })
        elif len(search) > 0 and len(search) != 12 and len(data_options) == 0 and search.isnumeric():
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
        elif len(search) > 0 and len(data_options) == 0 and not search.isnumeric() and search != '!':
            result.append({
                        'title':f"{_invalid_numbers_text}",
                        'valid': False,
                    })
        elif len(search) == 12 or len(data_options) == 0 and search.isnumeric():
            if not check:
                data = get_data.web_url(search)
                if data['sicepat']['status']['code'] == 400:
                    result.append({
                        'title':f"Resi Number not found. Please check again.",
                        'valid': False,
                    })
                else:
                    result.append({
                            'title': search,
                            'subtitle':f"Receiver: {data['sicepat']['result']['receiver_name']}  //  Sender: 📍{data['sicepat']['result']['sender']}  // valid✅",
                            'valid': True if search.isnumeric() and len(search) == 12 else False,
                            'arg' : search,
                            'variables' : {
                                    'resi_number' :  f"{data['sicepat']['result']['waybill_number']}",
                                    'new_resi' : True,
                                },
                            'mods':{
                                    'cmd' : {
                                        'subtitle' : 'Save resi number✓',
                                        'variables' : {
                                            'resi_number' : search,
                                            },
                                    }
                                }
                            })

    
    return result


"""Run Script Filter."""
def main():
    SEARCH = sys.argv[1] if len(sys.argv) >= 2 else None
    posts  = results(search=SEARCH)
    data = json.dumps({"rerun": 1,"items": posts }, indent=4) # make "rerun" : 0.2
    print(data)

if __name__ == '__main__':
    main()
    