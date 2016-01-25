 # imports are program code that are needed to run your program
import RPi.GPIO as GPIO  # import library for working with Raspberry's GPIO
import time  # needed to use sleep()


'''
Source file: button_events_v1.py

Start: sudo python button_events_v1.py

(v1) This code reads the status of a pin on the Raspberry PI. The pin is attached to a push button. 
The code is constantly polling the pin. When the button is pressed, the code will detect this. A '0' is 
read from the pin. An event is then created: 'pressed'. If the button is released the code will detect 
this too. A '1' is read from the pin and an event 'released' is created. These events are written to console.

Each time an event occurs: 
- write event to console

Input:		
- Raspberry PI pin state changes
Process:	
- Each time an event occurs: 
	- write event to console
Output:
- events to console

@author: Koen Warner
@version:  v1.1,  17 jun. 2014
(c) 2014 Koen Warner

'''

################################
# Global variables and set up  #
################################

# global variables
buttonPin = 4  # this will be an input pin to which the button is attached
				# in this case pin GPIO23 (which is pin number 16)
prev_state = 1  # set start state to 1 (button released)

# we're using the BCM pin layout of the Raspberry PI
GPIO.setmode(GPIO.BCM)

# set pin GPIO23 to be an input pin; this pin will read the button state
# activate pull down for pin GPIO23
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


############
# Run code #
############

# initialize event
event = 1

print "Button Events versie 1"

# keep on executing this loop forever (until someone stops the program)
if True:

	# read the current button state by reading pin GPIO23 on the Raspberry PI
	# the curr_state can be '0' (if button pressed) or '1' (if button released)
	curr_state = GPIO.input(buttonPin)

	# if state changed, take some actions
	if (curr_state != prev_state):  # state changed from '1' to '0' or from '0' to '1'
		if (curr_state == 1):  # button changed from pressed ('0') to released ('1')
			event = "uit"
			print event  # print event to console
		else:   # button changed from released ('1') to pressed ('0')
			event = "aan"  # print event to console
			print event
		prev_state = curr_state  # store current state

	time.sleep(0.02)  # sleep for a while, to prevent bouncing

# when exiting, reset all pins
GPIO.cleanup()
