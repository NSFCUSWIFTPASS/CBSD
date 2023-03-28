# (c) 2022 The Regents of the University of Colorado, a body corporate. Created by Stefan Tschimben.
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

import os
import time
import RPi.GPIO as GPIO

class LED(object):
    def __init__(self):
        if 'raspberrypi' not in os.uname():
            raise ValueError("Not an RPi, no LEDs present")
        #self._event = threading.Event()
        self._running = True

    def terminate(self):
        self._running = False
        os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness')

        # Terminating LED2 as well
        GPIO.cleanup()

    def register(self):
        # Solid LED to show the CBSD has been registered
        os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness')
        
    def inquiry(self):
        self._running = True
        while self._running:
            #if self._event.is_set():
            #    break
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)            
    
    def grant_request(self):
        self._running = True
        while self._running:
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.5)
        
    def heartbeat(self):
        # starts LED heartbeat pattern
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        pwm = GPIO.PWM(18, 10) # Pin number (NOT physical pin, physical pin is 12, Pin ID is 18), Frequency is 1 kHz
        pwm.start(50) #Duty cycle
        # https://learn.sparkfun.com/tutorials/raspberry-gpio/python-rpigpio-api
        #Modified such that LED2 is now the heartbeat and the system LED is used for other cases
        # os.system('echo heartbeat | sudo dd status=none of=/sys/class/leds/led0/trigger')

    
    def relinquish(self):
        self._running = True
        while self._running:
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.5)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.5)

        
    def deregister(self):
        os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
    
    def error(self):
        self._running = True
        while self._running:
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.2)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.2)
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness')
            time.sleep(0.5)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.3)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.2)
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            time.sleep(0.5)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.3)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.2)
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            time.sleep(0.5)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.2)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.4)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.5)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.1)
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.3)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.2)
            os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') 
            time.sleep(0.2)
            os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness')
            time.sleep(0.5)
