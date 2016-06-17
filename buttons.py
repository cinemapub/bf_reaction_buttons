#!/usr/bin/env python3
import datetime
import time
import sys
import select
import os
import RPi.GPIO as GPIO
import ConfigParser
import pygame
import urllib2

def read_config(cfgfile):
	global Config
	global last_push
	Config = ConfigParser.ConfigParser(allow_no_value=True)
	Config.read(cfgfile)
	last_push=time.time()
	for section in Config.sections():
		options=Config.options(section)
		pin=int(Config.get(section,"pin"))
		name=Config.get(section,"name")
		print("-- Setting button %s: %d (%s)" % (section,pin,name))
		GPIO.setup(pin , GPIO.IN)
		GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_react, bouncetime=500)

def button_react(input_pin): 
	global last_push
	global Config
	now = time.strftime("%H:%M:%S", time.localtime(time.time()))
	time_push=time.time()
	tdelta=time_push - last_push
	#print("%f ms since last push [%s - %s]" % (tdelta,last_push,time_push))
	last_push=time_push
	#if(time_push - last_push) < datetime.timedelta(0, 0, 1000):
	if tdelta <= .9:
		# too fast
		#print("too fast!")
		time.sleep(.5)
	else:
		print ("%s: button pressed: [%d]:%s" % (now,input_pin,GPIO.input(input_pin)))
		for section in Config.sections():
			options=Config.options(section)
			pin=int(Config.get(section,"pin"))
			if(pin == input_pin):
				name=Config.get(section,"name")
				
				play_sound=Config.get(section,"play_sound")
				if(play_sound):
					exec_sound(play_sound)
					
				run_command=Config.get(section,"run_command")
				if(run_command):
					exec_command(run_command)

				get_url=Config.get(section,"get_url")
				if(get_url):
					exec_url(get_url)

def exec_sound(sfile):
	bname=os.path.basename(sfile)
	print("SOUND: [%s]" % bname)
	pygame.mixer.music.load(sfile)
	pygame.mixer.music.play()
	#while pygame.mixer.music.get_busy() == True:
	#	continue
	
def exec_url(url):
	print("HTTP:  [%s]" % url)
	#response = urllib2.urlopen(url) # this is synchronous
	os.system("/usr/bin/curl -s \"%s\" -o /dev/null &" % url)

def exec_command(stext):
	print("EXEC:  [%s]" % stext)
	os.system(stext)

def main():
	os.system('clear') # clear screen
	#print("## set GPIO mode")
	GPIO.setmode(GPIO.BCM)
	print(GPIO.RPI_INFO)
	print("## initialize pygame mixer")
	pygame.mixer.init()
	os.system("amixer cset numid=3 1")
	os.system("amixer set PCM -- -000")
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
