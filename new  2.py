from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
import feedparser
newUpdates[] = null
GPIO.setup(4,GPIO.IN)
def checkFeed(i):
	if currentFeed[i] == previousFeed[i] || previousFeed[i] == null:
		return True
	else:
		return False
previousFeed[] = null
feed = ['http://paranatural.net/rss.php', 'http://feeds.feedburner.com/Explosm?format=xml', 'http://www.mspaintadventures.com/rss/rss.xml']
for x in range (0, 2):
	feedParse[x] = [feed[x], feedparser.parse[x]]
	currentFeed[x] = feedParse[x][1].entries[0].title
while True:
	lcd.clear
	for x in range (0, 2):
		if !checkFeed(x):   #If it returns false
			a = True
			b = 0
			while a == True:       #Add all updates to newUpdates[]
				if newUpdates[b] == null:
					newUpdates[b] = currentFeed[x]
					a = False
				else:
					b += 1
	prev_input = 0
	listNum = 0
	#take a reading
	input = GPIO.input(4)
	#if the last reading was low and this one high, print
	lcd.message('New Update!\n')
	if len(newUpdates[listNum]) > 16:
		length = len(newUpdates[listNum])
		for z in range (0, length - 15)         #Do the ticker thing! COOOLLLLLL
			input = GPIO.input(4)
			if input:                           #If button is pressed, get out of loop nao
				break
			else:
				continue
			lcd.clear
			lcd.message('New Update!\n')
			lcd.message(newUpdates[listNum][z:z+15])
			time.sleep(0.5)
	else:
		lcd.message(newUpdates[listNum])
	if ((not prev_input) and input):
		if newUpdates[listNum+1] == null:
			newUpdates = null
		else:
			listNum += 1
	#update previous input
	prev_input = input
	#slight pause to debounce i guess
	time.sleep(0.05)
	