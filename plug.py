import requests
import json
import time
import os
import wiringpi

# Initialize WiringPi
wiringpi.wiringPiSetupGpio()

relay1 = 23
relay2 = 22
relay3 = 27
relay4 = 17

wiringpi.pinMode(relay1, 1)
wiringpi.pinMode(relay2, 1)
wiringpi.pinMode(relay3, 1)
wiringpi.pinMode(relay4, 1)
wiringpi.digitalWrite(relay1, 1)
wiringpi.digitalWrite(relay2, 1)
wiringpi.digitalWrite(relay3, 1)
wiringpi.digitalWrite(relay4, 1)

serverurl = 'http://192.168.1.100:8080/getstatus'
plug_a_id = 1
plug_b_id = 2
plug_a_status = "NO STATUS"
plug_b_status = "NO STATUS"

while True:
    os.system('clear')
    print("eColi CLI Prototype - Plug Side")
    print("Plug 1 Status :", plug_a_status)
    print("Plug 2 Status :", plug_b_status)

    try:
        r = requests.post(serverurl, data={"plugid": str(plug_a_id)})
        getdata = r.json()
        if(getdata["plugstatus"] == "ON"):
            plug_a_status = "ON"
            wiringpi.digitalWrite(relay1, 0)
        elif(getdata["plugstatus"] == "OFF"):
            plug_a_status = "OFF"
            wiringpi.digitalWrite(relay1, 1)
        else:
            plug_a_status = "NO STATUS"
    except:
        plug_a_status = "CONNECTION ERROR"

    time.sleep(0.1)

    try:
        r = requests.post(serverurl, data={"plugid": str(plug_b_id)})
        getdata = r.json()
        if(getdata["plugstatus"] == "ON"):
            plug_b_status = "ON"
            wiringpi.digitalWrite(relay3, 0)
        elif(getdata["plugstatus"] == "OFF"):
            plug_b_status = "OFF"
            wiringpi.digitalWrite(relay3, 1)
        else:
            plug_b_status = "NO STATUS"
    except:
        plug_b_status = "CONNECTION ERROR"

    time.sleep(0.1)
