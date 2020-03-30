'''
	Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
from flask import Flask, render_template, flash, request
from flask_bootstrap import Bootstrap
from time import sleep
import sched, time


s = sched.scheduler(time.time, time.sleep)

app = Flask(__name__, instance_relative_config=False)
Bootstrap(app)
# App config.
#app.config.from_object('config.Config')

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define sensors GPIOs
button = 20
senPIR = 16

#define actuators GPIOs
ledRed = 13
ledYlw = 19
ledGrn = 26

shutter = 17
solenoid = 27

#initialize GPIO status variables
buttonSts = 0
senPIRSts = 0
ledRedSts = 0
ledYlwSts = 0
ledGrnSts = 0

shutterSts = 0
solonoidSts = 0

# Define button and PIR sensor pins as an input
GPIO.setup(button, GPIO.IN)   
GPIO.setup(senPIR, GPIO.IN)

# Define led pins as output
GPIO.setup(ledRed, GPIO.OUT)   
GPIO.setup(ledYlw, GPIO.OUT) 
GPIO.setup(ledGrn, GPIO.OUT)

GPIO.setup(shutter, GPIO.OUT)
GPIO.setup(solenoid, GPIO.OUT)

# turn leds OFF 
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledYlw, GPIO.LOW)
GPIO.output(ledGrn, GPIO.LOW)

GPIO.output(shutter, GPIO.HIGH)
GPIO.output(solenoid, GPIO.HIGH)

#Defining solenoid and shutter states

def solenoid_open(a='default'):
    GPIO.output(solenoid, GPIO.LOW)
#    print('Solenoid open', time.time(), a)

def solenoid_closed(a='default'):
    GPIO.output(solenoid, GPIO.HIGH)
#    print('Solenoid closed', time.time(), a)

def shutter_triggered(a='default'):
	GPIO.output(shutter, GPIO.LOW)
#    print('Shutter triggered', time.time(), a)

def shutter_reset(a='default'):
	GPIO.output(shutter, GPIO.HIGH)
#	print('Shutter triggered', time.time(), a)

#end of solenoid and shutter states

@app.route("/")
def index():


	# Read GPIO Status

	buttonSts = GPIO.input(button)
	senPIRSts = GPIO.input(senPIR)
	ledRedSts = GPIO.input(ledRed)
	ledYlwSts = GPIO.input(ledYlw)
	ledGrnSts = GPIO.input(ledGrn)

	templateData = {

      'button'  : buttonSts,
      'senPIR'  : senPIRSts,
      'ledRed'  : ledRedSts,
      'ledYlw'  : ledYlwSts,
      'ledGrn'  : ledGrnSts,
      }
	return render_template('index.html', **templateData)
	
# The function below is executed when someone requests a URL with the actuator name and action in it:
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'ledRed':
		actuator = ledRed
	if deviceName == 'ledYlw':
		actuator = ledYlw
	if deviceName == 'ledGrn':
		actuator = ledGrn
	
	if deviceName == 'shutter':
		actuator = shutter

	if deviceName == 'solonoid':
		actuator = solenoid
   
	if action == "on":
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		GPIO.output(actuator, GPIO.LOW)
 
	buttonSts = GPIO.input(button)
	senPIRSts = GPIO.input(senPIR)
	ledRedSts = GPIO.input(ledRed)
	ledYlwSts = GPIO.input(ledYlw)
	ledGrnSts = GPIO.input(ledGrn)
   
	templateData = {

	  'button'  : buttonSts,
      'senPIR'  : senPIRSts,
      'ledRed'  : ledRedSts,
      'ledYlw'  : ledYlwSts,
      'ledGrn'  : ledGrnSts,
	}
	return render_template('index.html', **templateData)


@app.route("/<droplet>", methods=['GET','POST'])
def droplet(droplet):
	shutter_delay = list(range(5, 40))

	dropdelay =  round(float(request.form['btwndrops'])/100,4)
	dropclosed = dropdelay + .01

	delay_amnt =  round(float(request.form['shutterdelay'])/100,4)
	shutterclosed = delay_amnt + 0.3
	
	s.enter(0.01,.05 , solenoid_open, kwargs={'a': 'drop 1 open'})
	s.enter(.05,0.01, solenoid_closed, kwargs={'a': 'drop 1 closed'})
	
	s.enter(dropdelay,0.05, solenoid_open, kwargs={'a': 'drop 2 open'})
	s.enter(dropclosed,.01, solenoid_closed, kwargs={'a': 'drop 2 closed'})
	
	s.enter(delay_amnt,0.3, shutter_triggered, kwargs={'a': 'shutter triggered'})
	s.enter(shutterclosed,0.01, shutter_reset, kwargs={'a': 'Shutter reset'})
	
	s.run()

	# #first drop
	# GPIO.output(solonoid, GPIO.LOW)
	# sleep(0.06)
	# GPIO.output(solonoid, GPIO.HIGH)
	# #delay for second drop
	# sleep(dropdelay)
	# #second drop
	# GPIO.output(solonoid, GPIO.LOW)
	# sleep(0.06)
	# GPIO.output(solonoid, GPIO.HIGH)
	# #Shutter triggered
	# sleep(delay_amnt)
	# GPIO.output(shutter, GPIO.LOW)
	# #GPIO pins reset
	# sleep(0.30)
	# GPIO.output(shutter, GPIO.HIGH)
	# GPIO.output(solonoid, GPIO.HIGH)



#	return( str(delay_amnt))
	return render_template('index.html', 
	dropdown_list=shutter_delay, 
	shutterdelay=delay_amnt, 
	btwndrops=dropdelay)




if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
