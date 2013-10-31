from bottle import get, run
import RPi.GPIO as GPIO
import ipget

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)

@get('/on')
def gpioON():
	GPIO.output(8, True)
	return "hogehoge"

@get('/off')
def gpioOFF():
	GPIO.output(8, False)
	return "OFOFOFOF"

hostip = ipget.ipget().ipaddr("eth0").split("/")[0]
run(host=hostip, port=8080)
# run(host='192.168.1.242', port=8080)




