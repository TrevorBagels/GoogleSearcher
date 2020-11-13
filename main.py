import os, time, datetime, sys
os.system("pip3 install -U selenium")
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

import configparser

class utilities:
	def numberize(value):
		try:
			v = float(value)
			v2 = int(value)
			if v-v2 == 0:
				return v2
			return v
		except:
			return value
	#for every value in a dictionary of strings, make the value an int or a float if needed
	def IntDictionary(d):
		for x in d:
			d[x] = utilities.numberize(d[x])
		return d

class Bot:
	def __init__(self):
		self.stopped = False
		#read the configuration file
		cfg = configparser.ConfigParser()
		cfg.read("config.ini")
		self.config = utilities.IntDictionary(dict(cfg["SETTINGS"]))

		#create logs folder if needed
		if os.path.isdir(os.getcwd()+"/logs") == False:
			os.mkdir("logs")
		#create log file name
		self.logFile = "logs/log_"+str(datetime.datetime.now()) + ".txt"
		#create the log file
		f = open(self.logFile, "w+")
		f.write("Log file for Google Bot")
		f.close()

		self.options = webdriver.ChromeOptions();
		if self.config["headless"]:
			self.options.add_argument('headless'); #only use if you want this to run in the background

	def log(self, txt, verbosity=0):
		if self.config["verbositylevel"] < verbosity:
			return
		print(txt)
		f = open(self.logFile, "a")
		f.write(f"\n{datetime.datetime.now().strftime('%m/%d_%H:%M:%S')}\t{txt}")
		f.close()
	def newSession(self):
		if self.stopped:
			return
		if hasattr(self, 'driver'):
			self.log("Quitting old session...")
			self.driver.quit()

		self.log("Creating new session...")
		time.sleep(5)
		#for mac
		self.driver = webdriver.Chrome(executable_path=os.getcwd()+"/chromedriver", options=self.options)
		#for linux
		#self.driver = webdriver.Chrome(options=self.options)

	def run(self, searchTerm, link):
		self.newSession()
		self.driver.get("https://www.google.com/")
		#find search field
		searchField = self.driver.find_elements_by_class_name("gLFyf")[0]
		#enter search term
		searchField.send_keys(searchTerm)
		#find search button
		searchButton = self.driver.find_elements_by_class_name("gNO89b")[1]
		#click search button
		searchButton.click()
		self.log(f"Searching term {searchTerm}")
		#now check each link on the page until we find the one that we want
		page = 1
		while True:
			if self.stopped:
				break
			found = False
			time.sleep(3)
			links = self.driver.find_elements_by_tag_name("a")
			for x in links:
				if self.stopped:
					break
				if x.get_attribute("href") != None:
					if self.config["exactlink"] == 0 and x.get_attribute("href").startswith(link) or self.config["exactlink"] == 1 and x.get_attribute('href') == link:
						self.log(f"Found {x.get_attribute('href')} on page {page} position {links.index(x)}.")
						x.click()
						found = True
						time.sleep(1)
						break
			if found:
				break
			if self.stopped:
				break
			page += 1
			self.log(f"Moving to page {page}", verbosity=1)
			self.driver.find_elements_by_xpath("//span[contains(text(), 'Next')][@style='display:block;margin-left:53px']")[0].click()
		time.sleep(1)
		return
	def exit(self, thing, thing2):
		self.stopped = True
		self.log("Stopping program...")
		if hasattr(self, 'driver'):
			self.log("Quitting old session...")
			self.driver.quit()
		sys.exit()

