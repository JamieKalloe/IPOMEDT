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


def autoRun():
    while True:
        global isRunning
        while isRunning == True:
            light()
            homef()
            tpid = getPid()
            #if (tpid != 1):
            #    sensor()
            #if (tpid == 1):
               # blink()
            #if (tpid != 1):
             #   blink()
            if (tpid == 1):
                #light()
                downf(102)
                time.sleep(0.25)
                upf(51)
                time.sleep(0.25)
                downf(102)
                time.sleep(0.25)
                homef()
                time.sleep(10)

            if (tpid == 2 and sensor() == 1):
                light()
                downf(1024)
                time.sleep(0.25)
                upf(512)
                time.sleep(0.25)
                downf(1024)
                time.sleep(0.25)
                homef()

            if (tpid == 3 and sensor() == 1):
                light()
                downf(1024)
                time.sleep(0.25)
                upf(512)
                time.sleep(0.25)
                downf(1024)
                time.sleep(0.25)
                homef()

            if (tpid == 4 and sensor() == 1):
                light()
                downf(1024)
                time.sleep(0.25)
                upf(512)
                time.sleep(0.25)
                downf(1024)
                time.sleep(0.25)
                homef()
				
            if (tpid == 5 and sensor() == 1):
                light()
                downf(1024)
                time.sleep(0.25)
                upf(512)
                time.sleep(0.25)
                downf(1024)
                time.sleep(0.25)
                homef()


thread.start_new_thread(autoRun, ())


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
                    print "Lights On"
                else:
                    print "Lights Off"
        prev_state = curr_state
	
        GPIO.cleanup()
    return curr_state

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
    homef()
    return render_template('index.html', )


@app.route('/lightcontrol.htm')
def lightControl():
    light()
    return redirect("/", code=302)


@app.route('/up.htm', methods=['GET'])
def up():
   # if (request.method == 'GET'):
        steps = request.args.get("steps")
        if steps is None:
            upf(steps=515)
        else:
            upf(int(steps))
    	return render_template('index.html', )


@app.route('/down.htm', methods=['GET'])
def down():
    if (request.method == 'GET'):
        steps = request.args.get("steps")
        if steps is None:
            downf(steps=515)
        else:
            downf(int(steps))
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
    global isRunning
    isRunning = True
    thread.start_new_thread(autoRun, ())
    return redirect(url_for('index'))


@app.route('/auto_off.htm')
def auto_off():
    global isRunning
    isRunning = False
    GPIO.cleanup()
    thread.start_new_thread(autoRun, ())
    return redirect(url_for('index'))


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
    sensor()
    return render_template('index.html', )


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
            else:  # button changed from released ('1') to pressed ('0')
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
