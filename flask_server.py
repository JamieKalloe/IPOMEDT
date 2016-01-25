from flask import Flask, render_template, request, redirect # to run Flask
import datetime
import time
import subprocess
import os # needed to check if events file exists
import RPi.GPIO as GPIO
import threading
import sys

exitFlag = 0
quitAll = 0
queueLock = threading.Lock()
threads = []
LeadingTreads = []

def readfile( file_name ):
	response = "OK"
	try:
		# check if event file already exists; if not, create it
		if not os.path.exists(file_name):
			response = "File does not exist"
		else:
			# open the button events event file for reading
			event_file = open(file_name, "r")
			# read all lines from the file into a Python list called 'lines'
			lines = [line.rstrip('\n') for line in event_file]	# strip new line character from each line in file	
			# close event file
			event_file.close()
	except:
		response = "There was an error reading the events "
	if(response == "OK"):
	    	return lines[0]
	else:
		return response

lightOn = 1;
# light on function 
def light(state="NULL"): 
	# to use Raspberry Pi board pin numbers 
	GPIO.setmode(GPIO.BOARD) 
	# set up GPIO output channel 
	GPIO.setup(26, GPIO.OUT)

	global lightOn
	lightPin = 26  
	if(state=="ON") or (lightOn == 0):
		print "Led On"
        	GPIO.output(lightPin,GPIO.HIGH)
		lightOn = 1
	else:
		print "Led Off"
        	GPIO.output(lightPin,GPIO.LOW) 
		lightOn = 0
        return 1

#turn light off
light()
GPIO.cleanup()

def rotateMotor(steps=0, direction="UP" ):
	global exitFlag, quitAll
	# Use BCM GPIO references
	# instead of physical pin numbers
	GPIO.setmode(GPIO.BCM)

	buttonPin = 25
	prev_state = 1
	GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	event = 1
	 
	# Define GPIO signals to use
	# Pins 18,22,24,26
	# GPIO24,GPIO25,GPIO8,GPIO7
	StepPins = [17,18,27,22]
	 
	# Set all pins as output
	for pin in StepPins:
	  GPIO.setup(pin,GPIO.OUT)
	  GPIO.output(pin, False)
	 
	# Define some settings
	StepCounter = 0
	WaitTime = 0.0025
	 
	# Define simple sequence
	
	#up
	StepCount1 = 4
	Seq1 = []
	Seq1 = range(0, StepCount1)
	
	Seq1[0] = [0,0,0,1]
	Seq1[1] = [0,0,1,0]
	Seq1[2] = [0,1,0,0]
	Seq1[3] = [1,0,0,0]
	
	#down
	StepCount2 = 4
	Seq2 = []
	Seq2 = range(0, StepCount2)	

	Seq2[0] = [1,0,0,0]
	Seq2[1] = [0,1,0,0]
	Seq2[2] = [0,0,1,0]
	Seq2[3] = [0,0,0,1]
	 
	# Choose a sequence to use
	if(direction == "UP"):
		Seq = Seq1
		StepCount = StepCount1
	else:
		Seq = Seq2
		StepCount = StepCount2
	
	if(steps == 0): 
		#Infinite loop
		while True:
		 curr_state = GPIO.input(buttonPin)
		 if (curr_state != prev_state):
			break

		 for pin in range(0, 4):		
			xpin = StepPins[pin]
			if Seq[StepCounter][pin]!=0:
				#print " Step %i Enable %i" %(StepCounter,xpin)
				GPIO.output(xpin, True)
			else:
				GPIO.output(xpin, False)
		 
		 StepCounter += 1
		 
		 # If we reach the end of the sequence
		 # start again
		 if (StepCounter==StepCount):
		   StepCounter = 0
		 if (StepCounter<0):
		   StepCounter = StepCount
		 
		 # Wait before moving on
		 time.sleep(WaitTime)
	else:
		# for loop
		for x in range(0, steps):
		  if(exitFlag != 0 and quitAll != 1):
			break
		  DownfromHomeIgnore = 0
		  if(direction != "UP"):
			DownfromHomeIgnore = 30
		  curr_state = GPIO.input(buttonPin)
		  if (x > DownfromHomeIgnore) and (curr_state != prev_state):
			break
		 
		  for pin in range(0, 4):
			xpin = StepPins[pin]
			if Seq[StepCounter][pin]!=0:
				#print " Step %i Enable %i" %(StepCounter,xpin)
				GPIO.output(xpin, True)
			else:
				GPIO.output(xpin, False)
		 
		  StepCounter += 1
		 
		  # If we reach the end of the sequence
		  # start again
		  if (StepCounter==StepCount):
		    StepCounter = 0
		  if (StepCounter<0):
		    StepCounter = StepCount
		 
		  # Wait before moving on
		  time.sleep(WaitTime)
		

	
	return 1

class StepThreads (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
	os.system('sudo shutdown -rF now')

class StopTreads (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
	os.system('sudo shutdown -h now')

# create a Flask objec called app
app = Flask(__name__)

# URL: http://IPADRESS:5000/
@app.route('/')
@app.route("/index.htm")
def index():
    	templateData = {
		'title' : "Control Panel",
		'xpos' : readfile('/boot/x.txt'),
		'ypos' : readfile('/boot/y.txt')
	}
	# return the main.html template to the web browser and pass into it the variables in the templateData dictionary
	return render_template('index.html', **templateData)

@app.route('/home.htm')
def home():
	buttonPin = 23
	prev_state = 1

	# we're using the BCM pin layout of the Raspberry PI
	GPIO.setmode(GPIO.BCM)

	# set pin GPIO23 to be an input pin; this pin will read the button state
	# activate pull down for pin GPIO23
	GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	# Define GPIO signals to use
	# Pins 18,22,24,26
	# GPIO17,GPIO18,GPIO27,GPIO22
	#17,18,27,22
	StepPins = [22,27,18,17]#deze aanpassen om om te draaien

	for pin in StepPins:
		GPIO.setup(pin,GPIO.OUT)
		GPIO.output(pin,False)

	# Wait some time to start
	time.sleep(0.5)

	# Define some settings
	StepCounter = 0
	WaitTime = 0.0015
	# Define simple sequence
	StepCount1 = 4
	Seq1 = []
	Seq1 = range(0, StepCount1)
	Seq1[0] = [1,0,0,0]
	Seq1[1] = [0,1,0,0]
	Seq1[2] = [0,0,1,0]
	Seq1[3] = [0,0,0,1]
	# Define advanced sequence
	# as shown in manufacturers datasheet
	StepCount2 = 8
	Seq2 = []
	Seq2 = range(0, StepCount2)
	Seq2[0] = [1,0,0,1]
	Seq2[1] = [1,1,0,0]
	Seq2[2] = [0,1,1,0]
	Seq2[3] = [0,0,1,1]
	Seq2[4] = [0,0,0,1]
	Seq2[5] = [1,0,0,1]
	Seq2[6] = [1,1,0,0]
	Seq2[7] = [0,1,1,0]

	#Full torque
	StepCount3 = 4
	Seq3 = []
	Seq3 = [3,2,1,0]
	Seq3[0] = [0,0,1,1]
	Seq3[1] = [1,0,0,1]
	Seq3[2] = [1,1,0,0]
	Seq3[3] = [0,1,1,0]
	# set
	Seq = Seq2
	StepCount = StepCount2

	# initialize event
	event = 1
	loop = True
	#while loop:
	while loop:
		for pin in range(0, 4):
			xpin = StepPins[pin]
			if Seq[StepCounter][pin]!=0:
				#print " Step %i Enable %i" %(StepCounter,xpin)
				GPIO.output(xpin, True)
			else:
				GPIO.output(xpin, False)
			StepCounter += 1
			curr_state = GPIO.input(buttonPin)
			if (curr_state != prev_state):
				if (curr_state == 0):
					event = "pressed"
					print event
					#sys.exit()
					loop = False
			prev_state = curr_state
			# If we reach the end of the sequence
			# start again
			if (StepCounter==StepCount):
				StepCounter = 0
			if (StepCounter<0):
				StepCounter = StepCount
			# Wait before moving on
			time.sleep(WaitTime)
	GPIO.cleanup()
	return render_template('index.html',)

@app.route('/lightcontrol.htm')
def lightControl():
	light()
	return redirect("/", code=302)

@app.route('/up.htm', methods=['GET'])
def up():
	if (request.method == 'GET'):
		steps = request.args.get("steps")
		if steps is None:
			rotateMotor(steps=2050,direction="UP")		
		else:		
			rotateMotor(int(steps),"UP")
	return render_template('index.html',)

@app.route('/down.htm', methods=['GET'])
def down():
	if (request.method == 'GET'):
		steps = request.args.get("steps")
		if steps is None:
			rotateMotor(steps=2050,direction="DOWN")		
		else:		
			rotateMotor(int(steps),"DOWN")
    	return render_template('index.html',)

@app.route('/xpos.htm')
def xpos():
	file_name = "/boot/x.txt"
    	return readfile(file_name)

@app.route('/ypos.htm')
def ypos():
    	file_name = "/boot/y.txt"
    	return readfile(file_name)

class autoAnimate (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
	global exitFlag, quitAll
	global rotateMotor
	rotateMotor(steps=6000, direction="DOWN")
        while exitFlag != 1 and quitAll != 1:
		rotateMotor(steps=5000, direction="DOWN")


@app.route('/auto_on.htm')
def auto_on(feedback=True):
	#Set Led on
	# Create new threads
	global exitFlag,threads
	exitFlag = 0
	#start tread
	thread = autoAnimate()
	thread.start()
	threads.append(thread)
	
	return render_template('auto_on.html',)


class autoAnimatetest (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
	global exitFlag, quitAll
	global rotateMotor
	
	buttonPin = 4  # this will be an input pin to which the button is attached
					# in this case pin GPIO23 (which is pin number 16)
	prev_state = 1  # set start state to 1 (button released)

	# we're using the BCM pin layout of the Raspberry PI
	GPIO.setmode(GPIO.BCM)

	# set pin GPIO23 to be an input pin; this pin will read the button state
	# activate pull down for pin GPIO23
	GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	# initialize event
	event = 1

	print "Button Events versie 1"

	# keep on executing this loop forever (until someone stops the program)
	while True:

		# read the current button state by reading pin GPIO23 on the Raspberry PI
		# the curr_state can be '0' (if button pressed) or '1' (if button released)
		curr_state = GPIO.input(buttonPin)
		# if state changed, take some actions
		while (curr_state != prev_state):  # state changed from '1' to '0' or from '0' to '1'
			if (curr_state == 1):  # button changed from pressed ('0') to released ('1')			
				light()
				auto_on(False)
				return 'Animation has been stopped'
			else:   # button changed from released ('1') to pressed ('0')			
				while (curr_state != prev_state):
					light("ON")
					rotateMotor(steps=5000, direction="UP")
					rotateMotor(steps=5000, direction="DOWN")				
					curr_state = GPIO.input(buttonPin) # store current state
					light()
		time.sleep(0.02)  # sleep for a while, to prevent bouncing
	# when exiting, reset all pins
	GPIO.cleanup()

@app.route('/auto_ontest.htm')
def auto_ontest(feedback=True):
	# Create new threads
	global exitFlag,threads
	exitFlag = 0
	#start tread
	thread = autoAnimatetest()
	thread.start()
	threads.append(thread)
	return render_template('auto_on.html',)


@app.route('/auto_off.htm')
def auto_off():
	#Set Led on for shutdown
	light()
	#Give thread exit flag	
	global exitFlag,threads
	exitFlag = 1
	#Wait for all threads to complete
	for t in threads:
	    t.join()
	time.sleep(1)
	exitFlag = 0
	return render_template('auto_on.html',)

@app.route('/shutdown.htm')
def shutdown():
	os.system('sudo shutdown -h now')
	thread = StopTreads()
	thread.start()
	
    	return 'The Raspberry Pi is shutting down.'

@app.route('/reboot.htm')
def reboot():
	os.system('sudo shutdown -r now')
	thread = StepThreads()
	thread.start()
	return 'The Raspberry Pi is rebooting.'
	

@app.route('/animatie1.htm')
def animatie1():
	rotateMotor(steps=2000, direction="DOWN")
	for x in range(0, 10):
		rotateMotor(steps=1000, direction="UP")
		rotateMotor(steps=1000, direction="DOWN")	
	
	rotateMotor(steps=0, direction="UP")
	return 'Animation completed'

@app.route('/animatietest.htm')
def animatietest():
	buttonPin = 4  # this will be an input pin to which the button is attached
					# in this case pin GPIO23 (which is pin number 16)
	prev_state = 1  # set start state to 1 (button released)

	# we're using the BCM pin layout of the Raspberry PI
	GPIO.setmode(GPIO.BCM)

	# set pin GPIO23 to be an input pin; this pin will read the button state
	# activate pull down for pin GPIO23
	GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	# initialize event
	event = 1

	print "Button Events versie 1"

	# keep on executing this loop forever (until someone stops the program)
	while True:

		# read the current button state by reading pin GPIO23 on the Raspberry PI
		# the curr_state can be '0' (if button pressed) or '1' (if button released)
		curr_state = GPIO.input(buttonPin)
		# if state changed, take some actions
		global exitFlag, quitAll
		while exitFlag != 1 and quitAll != 1:  # state changed from '1' to '0' or from '0' to '1'
			if (curr_state == 1):  # button changed from pressed ('0') to released ('1')
				auto_off()
			else:   # button changed from released ('1') to pressed ('0')
				event = "aan"  # print event to console
				light("ON")
				return 'AAN'
				animatie1()
				print event
			prev_state = curr_state  # store current state

		time.sleep(0.02)  # sleep for a while, to prevent bouncing
	# when exiting, reset all pins
	GPIO.cleanup()
	
	
@app.route('/kill.htm')
def kill():
	GPIO.cleanup()
        return 'Action stopped'

class checkLight (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
	global exitFlag, threads, autoAnimate,quitAll
	# global variables
	sensorPin = 24  # this will be an input pin to which the button is attached
					# in this case pin GPIO23 (which is pin number 16)
	prev_state = 0
	start_state = 0
  # set start state to 1 (button released)

	print "start job"
	while quitAll <= 0:
		# we're using the BCM pin layout of the Raspberry PI
		GPIO.setmode(GPIO.BCM)

		# set pin GPIO23 to be an input pin; this pin will read the button state
		# activate pull down for pin GPIO23
		GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		curr_state = GPIO.input(sensorPin)

		# if state changed, take some actions
		if (curr_state != prev_state):  
			if (curr_state == 0): 
				print "JOB Light ON"
				if(start_state == 1):
					print "JOB AUTO OFF"
					auto_off()	
					start_state = 0
				else:	
					time.sleep(1)
					auto_on(False)
					print "JOB AUTO ON"
					start_state = 1

			prev_state = curr_state  

		time.sleep(0.02)


# if the script was run directly from the command line
if __name__ == "__main__":
	# have the local host server listen on port 80, and report any errors
	app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False) # if permission denied; change port
