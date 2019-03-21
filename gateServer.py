from flask import Flask,request,jsonify
import json
import RPi.GPIO as GPIO
import time

# set raspberry pi pins
pin1 = 16
pin2 = 20
GPIO.setmode(GPIO.BCM)

# full closed positon
gateClosed = 10

# Gate class
# manages the gate
class Gate:
    def __init__(self):
        self.running = False # prevents multiple actions at same time
        self.status = 0 # integer represents gate location (0 = fully open, 10 fully closed)
        self.EmeStop = False # stops gate if true
        # Initialize the gate to be fully open
        GPIO.setup(pin2,GPIO.OUT)
        GPIO.output(pin2,False)
        time.sleep(35) # leave pin on for 35 seconds
        GPIO.output(pin2,True)


    # keeps track of gate position
    # open, stops and closes the gate
    # OPTIMIZE: gateController
    def gateController(self,PinNumber):
        GPIO.setup(PinNumber,GPIO.OUT) # set up pin
        if PinNumber == 20 and self.status != 0: # Check pin number and not already opened
            self.running = True # set the gate to running
            for a in range(self.status,-1, -1): # loop down to 0 (fully open)
                if self.EmeStop == True: # check to stop the gate
                    GPIO.output(PinNumber,True)
                    self.running = False # gate not running when stopped
                    break
                else:
                    time.sleep(1)
                    GPIO.output(PinNumber,False)
                    self.status = a
            GPIO.output(PinNumber,True)
            self.running = False
        # pin 16 is very similar to the pin 20
        elif PinNumber == 16  and self.status != 10:
            self.running = True
            for b in range(self.status, gateClosed +1): # loop up to 10 (fully closed)
                if self.EmeStop == True:
                    GPIO.output(PinNumber,True)
                    self.running = False
                    break
                else:
                    time.sleep(1)
                    GPIO.output(PinNumber,False)
                    self.status = b
            GPIO.output(PinNumber,True)
            self.running = False

    # returns the gate position
    def gatePostiton(self):
        return str(TheGate.status)


# create a gate object
TheGate = Gate()


# API
app = Flask(__name__)
@app.route('/gate' ,methods= ['GET','POST'])
def gate():
    # POST request
    if request.method == "POST":
        # JSON user info
        Some_json = request.json
        Command = Some_json['gate']
        # three commands exist (open,close and stop)
        if (Command == "close" and TheGate.running == False): # gate must not be running
            TheGate.EmeStop = False
            TheGate.gateController(pin1) # call gateController with the opening pin

        elif (Command == "open" and TheGate.running == False):
            TheGate.EmeStop = False
            TheGate.gateController(pin2)

        elif (Command == "stop"):
            TheGate.EmeStop = True
        # TODO: change the JSON response to be a stream of gate positions
        return jsonify({"postion":TheGate.gatePostiton()})
        
    # GET request
    elif request.method == "GET":
        # responed with gate position
        return jsonify({"postion":TheGate.gatePostiton()})

#app.run(host="YourAddress",port=YourPort, ssl_context=("PublicKey","PrivKey")) #WAN connection
#app.run(host="YourAddress",port=YourPort) # LAN connection
