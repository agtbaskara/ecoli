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

while True:
    os.system('clear')
    print("eColi CLI Prototype - Plug Program")
    try:
        r = requests.post(serverurl, data={"plugid": str(plug_a_id)})
        getdata = r.json()
        if(getdata["plugstatus"] == "ON"):
            print("Plug 1 Status : ON")
            wiringpi.digitalWrite(relay1, 0)
        elif(getdata["plugstatus"] == "OFF"):
            print("Plug 1 Status : OFF")
            wiringpi.digitalWrite(relay1, 1)
        else:
            print("Plug 1 Status : No Status")
    except:
        print("Plug 1 Status : Connection Error")

    time.sleep(0.1)

    try:
        r = requests.post(serverurl, data={"plugid": str(plug_b_id)})
        getdata = r.json()
        if(getdata["plugstatus"] == "ON"):
            print("Plug 2 Status : ON")
            wiringpi.digitalWrite(relay3, 0)
        elif(getdata["plugstatus"] == "OFF"):
            print("Plug 2 Status : OFF")
            wiringpi.digitalWrite(relay3, 1)
        else:
            print("Plug 2 Status : No Status")
    except:
        print("Plug 2 Status : Connection Error")

    time.sleep(0.1)
