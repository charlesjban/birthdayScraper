# import dependencies
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import time
from random import randint

print("\n\n\n")

# user input birthday
# convert to a date, print message if input not in correct format
birthdayOK = False
while birthdayOK == False:
	birthdayInput = input("Please enter your date of birth, in the format dd/mm/yyyy : ")
	# time breaks used to enhance user experience
	time.sleep(1)
	print("\n\n")
	try:
		# convert to datetime
		dateOfBirth = datetime.datetime.strptime(birthdayInput, "%d/%m/%Y")
		birthdayOK = True
	except ValueError:
		print("Please enter DOB in correct format")
message = "You were born on {:%A, %B %d, %Y}"
print(message.format(dateOfBirth))

print("\n\n")
time.sleep(1.5)

# calculate and print days alive
present = datetime.datetime.today()
timeAlive = present - dateOfBirth
daysAlive = str(timeAlive).split(" ")[0]
print("You have been alive for %s days!"%daysAlive)
time.sleep(1.5)
print("\n\n")
# calculate and print days till next birthday
currentYear = datetime.datetime.strftime(present,"%Y")
nextBirthday = birthdayInput[:-4]+currentYear
nextBirthday = datetime.datetime.strptime(nextBirthday, "%d/%m/%Y")
timeTillNext = nextBirthday - present
daysTillNextBday = int(str(timeTillNext).split(" ")[0])
#change next birthday to folowing year, if birthday has already passed this year
if daysTillNextBday < 0:
	nextBirthday = "%s%s"%(birthdayInput[:-4],str(int(currentYear)+1))
	nextBirthday = datetime.datetime.strptime(nextBirthday, "%d/%m/%Y")
	timeTillNext = nextBirthday - present
	daysTillNextBday = int(str(timeTillNext).split(" ")[0])
message = "Your next birthday is on a {:%A}"
print(message.format(nextBirthday))
time.sleep(1)
print("And is in %d days."%daysTillNextBday)
time.sleep(1.5)
print("\n\n\nNice.")
time.sleep(1)


print("\n\nEver wondered who you share a birthday with...?")

# format date and month strings to paste into web browser
month = datetime.datetime.strftime(dateOfBirth, "%B")
date = datetime.datetime.strftime(dateOfBirth, "%d")
if date.startswith('0'):
	date = date[-1]
# instantiate web browser
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome("./chromedriver", options=chrome_options)
# access website
driver.get("https://www.who2.com/born-on/%s-%s/"%(month,date))
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

# create arrays to store names and info
nameList = []
summaries = []
# search for HTML containers which contain names and info, add to lists
for a in soup.findAll('li', href=False, attrs={'class':'archive-list-item'}):
	name = a.find('h3', attrs={'class':'entry-title'})
	nameList.append(name.text)
	summary = a.find('div', attrs={'class': 'entry-summary'})
	summaries.append(summary.text)
driver.close()

# format and print out each item
print("\n\nHere are some famous examples...")
time.sleep(1)
for i in range(0, len(nameList)):
	name = nameList[i]
	summary = summaries[i]	
	try:
		splitName = name.split(",")
		firstNameFull = splitName[1].split("\n")
		firstName = firstNameFull[0]
		fullName = firstName + " " + splitName[0]
		year = name[-6:-2]
		print(fullName.strip("\n"), "-", year, "\t", summary.strip("\n").strip("\t"))
		time.sleep(1)
	except:
		pass

time.sleep(1.5)
print("\n\n\n")

# pick a random farewell and print
goodbyes = {1:"Thanks, bye!", 2:"Here's to many more birthdays...!", 3:"Adios!",4:"See ya later alligator!", 5:"Au-revoir!"}
randomNumber = randint(1,5)
print(goodbyes[randomNumber],"\n\n\n")
