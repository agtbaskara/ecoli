import wiringpi
import time

# Initialize WiringPi
wiringpi.wiringPiSetupGpio()

relay1 = 17
relay2 = 18
relay3 = 15
relay4 = 14

wiringpi.pinMode(relay1,1)
wiringpi.pinMode(relay2,1)
wiringpi.pinMode(relay3,1)
wiringpi.pinMode(relay4,1)
wiringpi.digitalWrite(relay1,1)
wiringpi.digitalWrite(relay2,1)
wiringpi.digitalWrite(relay3,1)
wiringpi.digitalWrite(relay4,1)

counter = 0
while counter<5:
    wiringpi.digitalWrite(relay1,0)
    time.sleep(3)
    wiringpi.digitalWrite(relay1,1)
    time.sleep(3)
    counter=counter+1


