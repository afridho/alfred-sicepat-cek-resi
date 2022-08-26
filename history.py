# -*- coding: utf-8 -*-

import sys
import requests
import os
import datetime as dt
from workflow import Workflow
import json


def main(wf):
    fileObject = open("no_resi.json", "r")
    jsonContent = fileObject.read()
    aList = json.loads(jsonContent)

    wf.add_item(
                 title=aList['resi'],
                 subtitle=aList['time'],
                 arg=aList['resi'],
                 valid='True',
                 )

   
 # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
 wf = Workflow()
 sys.exit(wf.run(main))

