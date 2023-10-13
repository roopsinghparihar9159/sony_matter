#!/usr/bin/python3
import time, os
from datetime import datetime

while(True):
        os.system("python3 mainNONdrm.py running karan")
        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("dt= ", dt_string)
        time.sleep(30)