import requests
import json
import time
import wiringpi

# Initialize WiringPi
wiringpi.wiringPiSetupGpio()

relay1 = 23
relay2 = 22
relay3 = 27
relay4 = 17

wiringpi.pinMode(relay1,1)
wiringpi.pinMode(relay2,1)
wiringpi.pinMode(relay3,1)
wiringpi.pinMode(relay4,1)
wiringpi.digitalWrite(relay1,1)
wiringpi.digitalWrite(relay2,1)
wiringpi.digitalWrite(relay3,1)
wiringpi.digitalWrite(relay4,1)

serverurl = 'http://192.168.43.29:8080/getstatus'
myId1 = 123
myId2 = 456

while True:
    try:
        r = requests.post(serverurl, data={"plugId": str(myId1)})
        getdata = r.json()
        if(getdata["plugStatus"] == "on"):
            print("Plug 1 On")
            wiringpi.digitalWrite(relay1,0)
        elif(getdata["plugStatus"] == "off"):
            print("Plug 1 Off")
            wiringpi.digitalWrite(relay1,1)
        else:
            print("Plug 1 No Status")
    except:
        print("Plug 1 Connection Error")

    time.sleep(0.1)

    try:
        r = requests.post(serverurl, data={"plugId": str(myId2)})
        getdata = r.json()
        if(getdata["plugStatus"] == "on"):
            print("Plug 2 On")
            wiringpi.digitalWrite(relay2,0)
        elif(getdata["plugStatus"] == "off"):
            print("Plug 2 Off")
            wiringpi.digitalWrite(relay2,1)
        else:
            print("Plug 2 No Status")
    except:
        print("Plug 2 Connection Error")

    time.sleep(0.1)
