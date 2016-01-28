import os  # needed to check if events file exists
import threading
import time
import thread
import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect, url_for  # to run Flask
from pid import getPid

exitFlag = 0
quitAll = 0
queueLock = threading.Lock()
threads = []
LeadingTreads = []

isRunning = False
stopChecking = False
tryToStart = False
individualAnim = False

def autoRun():
    tpid = getPid()
    print "Raspberry id ", tpid
    global isRunning
    while tryToStart == True:
        if tpid != 1 and checkSensor() == 1:
            isRunning = True
            # setOn()
        elif tpid != 1:
            isRunning = False
            if stopChecking == True:
                break
        elif tpid == 1 and isRunning is False:
            isRunning = True

        print "isRunning is", isRunning
        while isRunning == True:

            if tpid != 1:
                time.sleep(1)

            if tpid == 1:
                light("ON")
                homef()
                print("2. Down 400")
                time.sleep(0.25)
                print("4. Up 400")
                # upf(400)
                print("5. Sleep 0.25")
                time.sleep(0.25)
                print("6. Down 400")
                downf(400)
                print("7. Sleep 0.25")
                time.sleep(0.25)

            if tpid == 2:
                light("ON")
                homef()
                print("2. Down 400")
                time.sleep(0.25)
                print("4. Up 400")
                # upf(400)
                print("5. Sleep 0.25")
                time.sleep(0.25)
                print("6. Down 400")
                downf(400)
                print("7. Sleep 0.25")
                time.sleep(0.25)

            if tpid == 3:
                light("ON")
                homef()
                print("2. Down 400")
                time.sleep(0.25)
                print("4. Up 400")
                # upf(400)
                print("5. Sleep 0.25")
                time.sleep(0.25)
                print("6. Down 400")
                downf(400)
                print("7. Sleep 0.25")
                time.sleep(0.25)

            if tpid == 4:
                light("ON")
                homef()
                print("2. Down 400")
                time.sleep(0.25)
                print("4. Up 400")
                # upf(400)
                print("5. Sleep 0.25")
                time.sleep(0.25)
                print("6. Down 400")
                downf(400)
                print("7. Sleep 0.25")
                time.sleep(0.25)
				
            if tpid == 5:
                light("ON")
                homef()
                print("2. Down 400")
                time.sleep(0.25)
                print("4. Up 400")
                # upf(400)
                print("5. Sleep 0.25")
                time.sleep(0.25)
                print("6. Down 400")
                downf(400)
                print("7. Sleep 0.25")
                time.sleep(0.25)
            break


# thread.start_new_thread(autoRun, ())


def blink():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(26, GPIO.OUT)

    speed = 5

    GPIO.output(26, True)
    time.sleep(speed)

    GPIO.cleanup()


def sensor():
	buttonPin = 5
	prev_state = 1

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	while True:

		curr_state = GPIO.input(buttonPin)
        	if (curr_state != prev_state):

        		if (curr_state == 1):
                		print "Lights On ", curr_state
			else:
				print "Lights Off ", curr_state
	 	prev_state = curr_state

        GPIO.cleanup()
        return curr_state

def checkSensor():
    buttonPin = 5
    prev_state = 1
    sensorstate = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    curr_state = GPIO.input(buttonPin)
    sensorstate = curr_state

    return sensorstate


def setOff():
    global isRunning
    isRunning = False
    global stopChecking
    stopChecking = True
    global tryToStart
    tryToStart = False
    GPIO.cleanup()
    thread.start_new_thread(autoRun, ())

def setOn():
    global isRunning
    isRunning = True
    global stopChecking
    stopChecking = False
    global tryToStart
    tryToStart = True
    thread.start_new_thread(autoRun, ())

def readfile(file_name):
    response = "OK"
    try:
        # check if event file already exists; if not, create it
        if not os.path.exists(file_name):
            response = "File does not exist"
        else:
            # open the button events event file for reading
            event_file = open(file_name, "r")
            # read all lines from the file into a Python list called 'lines'
            lines = [line.rstrip('\n') for line in event_file]  # strip new line character from each line in file
            # close event file
            event_file.close()
    except:
        response = "There was an error reading the events "
    if (response == "OK"):
        return lines[0]
    else:
        return response


lightOn = 1


# light on function
def light(state="NULL"):
    # to use Raspberry Pi board pin numbers
    GPIO.setmode(GPIO.BCM)
    # set up GPIO output channel
    GPIO.setup(7, GPIO.OUT)

    global lightOn
    lightPin = 7
    if (state == "ON") or (lightOn == 0):
        print "Led On"
        GPIO.output(lightPin, GPIO.HIGH)
        lightOn = 1
    else:
        print "Led Off"
        GPIO.output(lightPin, GPIO.LOW)
        lightOn = 0
    return 1


# turn light off
light()
GPIO.cleanup()

def individual_anim():
    while individualAnim == True:
            homef()
            print("2. Down 400")
            time.sleep(0.25)
            print("4. Up 400")
            # upf(400)
            print("5. Sleep 0.25")
            time.sleep(0.25)
            print("6. Down 400")
            downf(400)
            print("7. Sleep 0.25")
            time.sleep(0.25)

def homef():
    buttonPin = 23
    prev_state = 1

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    omw = 1
    while omw:
       # GPIO.setmode(GPIO.BCM)
       # GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        curr_state = GPIO.input(buttonPin)
        if (curr_state != prev_state):
            print "home"
            omw = 0
            prev_state = curr_state
            if isRunning is True:
                downf(50)
            return 1
        upf()

    return 1

def downf(steps=515):
    GPIO.setmode(GPIO.BCM)
    buttonPin = 23
    prev_state = 1
    ControlPin = [17, 18, 27, 22]

    for pin in ControlPin:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    seq = [[1, 0, 0, 0],
           [1, 1, 0, 0],
           [0, 1, 0, 0],
           [0, 1, 1, 0],
           [0, 0, 1, 0],
           [0, 0, 1, 1],
           [0, 0, 0, 1],
           [1, 0, 0, 1]]

    try:
        for i in range(1 * steps):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            curr_state = GPIO.input(buttonPin)
            if prev_state != curr_state:
                break
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(ControlPin[pin], seq[halfstep][pin])
                time.sleep(0.0025)
            print(i)
    except KeyboardInterrupt:
        GPIO.cleanup()

    # GPIO.cleanup()


def upf(steps=515):
    GPIO.setmode(GPIO.BCM)
    buttonPin = 23
    prev_state = 1

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    ControlPin = [17, 18, 27, 22]

    for pin in ControlPin:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    seq = [[0, 0, 0, 1],
           [0, 0, 1, 1],
           [0, 0, 1, 0],
           [0, 1, 1, 0],
           [0, 1, 0, 0],
           [1, 1, 0, 0],
           [1, 0, 0, 0],
           [1, 0, 0, 1]]
    try:
        for i in range(1 * steps):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            curr_state = GPIO.input(buttonPin)
            if prev_state != curr_state:
                break
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(ControlPin[pin], seq[halfstep][pin])
                time.sleep(0.0025)
            print(i)
    except KeyboardInterrupt:
        GPIO.cleanup()

    # GPIO.cleanup()


class StepThreads(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        os.system('sudo shutdown -rF now')


class StopTreads(threading.Thread):
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
        'title': "Control Panel",
        'xpos': readfile('/boot/x.txt'),
        'ypos': readfile('/boot/y.txt')
    }
    # return the main.html template to the web browser and pass into it the variables in the templateData dictionary
    return render_template('index.html', **templateData)


@app.route('/home.htm')
def home():
    global tryToStart
    if tryToStart == False:
        homef()
    else:
        print("Auto_on is running, cannot go to home!")
    return render_template('index.html', )


@app.route('/lightcontrol.htm')
def lightControl():
    global tryToStart
    if tryToStart == False:
        light()
    else:
        print("Auto_on is running, cannot turn led on/off")
    return redirect("/", code=302)


@app.route('/up.htm', methods=['GET'])
def up():
    global tryToStart
    if tryToStart == False:
        steps = request.args.get("steps")
        if steps is None:
            upf(steps=515)
        else:
            upf(int(steps))
    else:
        print("Auto_on is running, cannot go up!")
    return render_template('index.html', )


@app.route('/down.htm', methods=['GET'])
def down():
    global tryToStart
    if tryToStart == False:
        if (request.method == 'GET'):
            steps = request.args.get("steps")
            if steps is None:
                downf(steps=515)
            else:
                downf(int(steps))
    else:
        print("Auto_on is running, cannot go down!")
    return render_template('index.html', )


@app.route('/xpos.htm')
def xpos():
    file_name = "/boot/x.txt"
    return readfile(file_name)


@app.route('/ypos.htm')
def ypos():
    file_name = "/boot/y.txt"
    return readfile(file_name)


class autoAnimate(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global exitFlag, quitAll
        global rotateMotor
        rotateMotor(steps=6000, direction="DOWN")
        while exitFlag != 1 and quitAll != 1:
            rotateMotor(steps=5000, direction="DOWN")


@app.route("/auto_on.htm")
def auto_on():
    #global isRunning
    #isRunning = True
    #thread.start_new_thread(autoRun, ())
    setOn()
    return redirect(url_for('index'))


@app.route('/auto_off.htm')
def auto_off():
    #global isRunning
    #isRunning = False
    #GPIO.cleanup()
    #thread.start_new_thread(autoRun, ())
    setOff()
    return redirect(url_for('index'))


@app.route('/shutdown.htm')
def shutdown():
    global tryToStart
    if tryToStart == False:
        os.system('sudo shutdown -h now')
        thread = StopTreads()
        thread.start()
    else:
        print("Auto_on is running, cannot shutdown!")
        return redirect(url_for('index'))


    return 'The Raspberry Pi is shutting down.'


@app.route('/reboot.htm')
def reboot():
    global tryToStart
    if tryToStart == False:
        os.system('sudo shutdown -r now')
        thread = StepThreads()
        thread.start()
    else:
        print("Auto_on is running, cannot reboot!")
        return redirect(url_for('index'))
    return 'The Raspberry Pi is rebooting.'


@app.route('/individual_animation.htm')
def individual_animation():
    global tryToStart
    global individualAnim
    individualAnim = True
    if tryToStart == False:
        thread.start_new_thread(individual_anim, ())
    else:
        print("Auto_on is running, cannot start another animation!")
    return render_template('index.html', )

@app.route('/stop_indivi_anim.htm')
def stop_indivi_anim():
    global individualAnim
    individualAnim = False
    GPIO.cleanup()
    thread.start_new_thread(individual_anim, ())
    return render_template('index.html', )

class checkLight(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global exitFlag, threads, autoAnimate, quitAll
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
                    if (start_state == 1):
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
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)  # if permission denied; change port
