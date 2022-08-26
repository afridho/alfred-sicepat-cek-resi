# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime
import sys

if len(sys.argv) > 1:
    no_resi = sys.argv[1]
else:
    no_resi = 'null'
    print('Nomor Resi Not Saved.')

def save_resi(x):
    if x != 'null':
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

        aDict = {"resi":no_resi, "time": time_now}
        jsonString = json.dumps(aDict)
        jsonFile = open("no_resi.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        print('Nomor Resi saved.')

save_resi(no_resi)