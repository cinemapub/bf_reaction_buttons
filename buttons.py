#!/usr/bin/env python3
import datetime
import time
import sys
import select
import os
import RPi.GPIO as GPIO

def button_press(event):
	print (event.pin_num)


def unregister_buttons(buttonlistener):
	buttonlistener.deactivate()


def register_buttons(buttonlistener):
	for i in range(8):
		buttonlistener.register(i, pifacecad.IODIR_FALLING_EDGE, button_press)
	buttonlistener.activate()

def main():
	
	GPIO.setmode(GPIO.BCM)

	buttons = [17,27,22,18,23,24]
	
	for b in buttons:
		print ("setting pin", b,"as input")
		#GPIO.setup(b , GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(b , GPIO.IN)
	# loop forever
	try:  
		while True:            # this will carry on until you hit CTRL+C 
			status = []
			for b in buttons:
				status.append("%d: [%d]" % (b,GPIO.input(b)) )
			print("Status: ", ', '.join(status))
			time.sleep(1)         # wait 0.1 seconds  

	except KeyboardInterrupt:  
		GPIO.cleanup()         # clean up after yourself  
	
if __name__ == "__main__":
	main()
