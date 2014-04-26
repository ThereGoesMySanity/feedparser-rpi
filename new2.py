import RPi.GPIO as GPIO
GPIO.setwarnings(False)
from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
import linecache
import time
import feedparser
import signal
checked = False
lcd = Adafruit_CharLCD()
newUpdates = []
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)
feedParse = []
currentFeed = []
previousFeed = []
feed = []
file = open('updates.txt', 'r+')
oldList = file.read()
feedLen = len(feed)
with open('feeds.txt', 'r') as f:
	for line in f:
		feed.append(line)
for f in range (feedLen):
	feedParse.append(feedparser.parse(feed[f]))
	currentFeed.append(feedParse[f].entries[0].title)
	previousFeed.append('0')
	currentTitle = feedParse[f].feed.title
class AlarmException(Exception):
	pass
def alarmHandler(signum, frame):
	raise AlarmException
def nonBlockingRawInput(prompt='', timeout=5):
	signal.signal(signal.SIGALRM, alarmHandler)
	signal.alarm(timeout)
	try:
		text = raw_input(prompt)
		signal.alarm(0)
		return text
	except AlarmException:
		print '\nPrompt Timeout.'
	signal.signal(signal.SIGALRM, signal.SIG_IGN)
	return ''
def checkFeed(i):
	if currentFeed[i] == previousFeed[i]:
		return False
	else:
		previousFeed[i] = currentFeed[i]
		return True
while True:
	list = oldList.split(', ')
	
	for f in range(feedLen):
		feedParse[f] = feedparser.parse(feed[f])
		currentFeed[f] = feedParse[f].entries[0].title
	lcd.clear
	for x in range (feedLen):
		if checkFeed(x):                       #If it returns false
			checked = False
			print '==> ', currentFeed,'\n ==> ' , list, '\n ==>', oldList 
			if not currentFeed[x] in list[x]:
				newUpdates.append(currentFeed[x])
	if newUpdates: 
		if len(newUpdates[0]) > 16:
			length = len(newUpdates[0])
			for z in range (length - 15):           #Do the ticker thing! COOOOOOL
				input = GPIO.input(4)
				lcd.clear()
				lcd.message('New Update!\n')
				lcd.message(newUpdates[0][z:z+16])
				time.sleep(0.5)
		else:
			lcd.clear()
			lcd.message('New Update!')
			lcd.message(newUpdates[0])
		test = nonBlockingRawInput('Clear log?\n').lower()
		if test == 'yes':
			del(newUpdates[0])
			lcd.clear()
		else:
			print test

	elif not checked:
		checked = True
		lcd.clear()
		lcd.message('No new updates')
	#slight pause to debounce i guess
	time.sleep(0.05)
	file.seek(0)
	oldList = ', '.join(currentFeed)
	file.write(oldList)
file.close
