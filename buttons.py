#!/usr/bin/env python3
import datetime
import time
import sys
import select
import os
import RPi.GPIO as GPIO
import ConfigParser
import pygame

def read_config(cfgfile):
	global Config
	Config = ConfigParser.ConfigParser()
	Config.read(cfgfile)
	for section in Config.sections():
		options=Config.options(section)
		pin=int(Config.get(section,"pin"))
		name=Config.get(section,"name")
		print("-- Setting button %s: %d (%s)" % (section,pin,name))
		GPIO.setup(pin , GPIO.IN)
		GPIO.add_event_detect(pin, GPIO.RISING, callback=button_react, bouncetime=500)

def button_react(input_pin): 
	global Config
	now = time.strftime("%H:%M:%S", time.localtime(time.time()))
	print ("%s: button pressed: [%d]:%s" % (now,input_pin,GPIO.input(input_pin)))
	for section in Config.sections():
		options=Config.options(section)
		pin=int(Config.get(section,"pin"))
		if(pin == input_pin):
			name=Config.get(section,"name")
			play_sound=Config.get(section,"play_sound")
			print("Play sound [%s]" % play_sound)
			exec_sound(play_sound)
			run_command=Config.get(section,"run_command")
			print("Run command [%s]" % run_command)
			exec_command(run_command)

def exec_sound(sfile):
	pygame.mixer.music.load(sfile)
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
		continue
	
def exec_command(stext):
	os.system(stext)

def main():
	
	print("## set GPIO mode")
	GPIO.setmode(GPIO.BCM)
	print(GPIO.RPI_INFO)
	print("## initialize pygame mixer")
	pygame.mixer.init()
	print("## read config")
	read_config("config/buttons.ini")

	try:  
		while True:            # this will carry on until you hit CTRL+C 
			#status = []
			#for b in buttons:
			#	status.append("%d: [%d]" % (b,GPIO.input(b)) )
			#print("Status: ", ', '.join(status))
			time.sleep(1)         # wait 0.1 seconds  

	except KeyboardInterrupt:  
		GPIO.cleanup()         # clean up after yourself  
	
if __name__ == "__main__":
	main()
