import wiringpi
import time

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

for i in range(0,5):
    print("Relay 1 ON")
    wiringpi.digitalWrite(relay1,0)
    time.sleep(1)
    print("Relay 2 ON")
    wiringpi.digitalWrite(relay2,0)
    time.sleep(1)
    print("Relay 3 ON")
    wiringpi.digitalWrite(relay3,0)
    time.sleep(1)
    print("Relay 4 ON")
    wiringpi.digitalWrite(relay4,0)
    time.sleep(1)
    print("All Relay OFF")
    wiringpi.digitalWrite(relay1,1)
    wiringpi.digitalWrite(relay2,1)
    wiringpi.digitalWrite(relay3,1)
    wiringpi.digitalWrite(relay4,1)
    time.sleep(1)

