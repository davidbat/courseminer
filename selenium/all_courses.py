#!/usr/bin/env python
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import time
from bs4 import BeautifulSoup

sem_hash =  {   'Fall 2009 (View only)':'Fall_2009',
				'Fall 2010 (View only)':'Fall_2010',
				'Fall 2011 (View only)':'Fall_2011',
				'Fall 2012 (View only)':'Fall_2012',
				'Spring 2010 (View only)':'Spring_2010',
				'Spring 2011 (View only)':'Spring_2011',
				'Spring 2012 (View only)':'Spring_2012',
				'Spring 2013':'Spring_2013',
				'Summer 1 2010 (View only)':'Summer_1_2010',
				'Summer 1 2011 (View only)':'Summer_1_2011',
				'Summer 1 2012 (View only)':'Summer_1_2012',
				'Summer 2 2010 (View only)':'Summer_2_2010',
				'Summer 2 2011 (View only)':'Summer_2_2011',
				'Summer 2 2012 (View only)':'Summer_2_2012',
				'Summer Full 2010 (View only)':'Summer_Full_2010',
				'Summer Full 2011 (View only)':'Summer_Full_2011',
				'Summer Full 2012 (View only)':'Summer_Full_2012' }

wait_time = 10
wait_low = 5
fp = webdriver.FirefoxProfile()
fp.set_preference('browser.sessionstore.postdata', 1)
fp = webdriver.FirefoxProfile('/home/dave/.mozilla/firefox/yoijpybx.default/')

driver = webdriver.Firefox(fp)

path = "/home/dave/Dropbox/my stuff/dm/courseminer/selenium/out/"

def my_test(ids, sem):
	
	driver.set_page_load_timeout(30)
	driver.get('https://myneu.neu.edu/')
	time.sleep(wait_time)
	assert "myNEU" in driver.title
	user = driver.find_element_by_name("user")
	user.send_keys("batelu.d")
	passw = driver.find_element_by_name("pass")
	passw.send_keys("floorPOD")
	driver.find_element_by_xpath("//input[@value='Login']").click()
	# Wait for page
	time.sleep(wait_time)
	#wait = ui.WebDriverWait(driver,10)
	driver.find_element_by_xpath("//div[@class='taboff']").click()
	driver.find_element_by_xpath("(//span[@id='p_chan_text']/p/a/b)[3]").click()
	# waitForPopUp
	time.sleep(wait_time)
	driver.switch_to_window("EntireSched")
	assert "Dynamic Schedule" in driver.title

	el = driver.find_element_by_id('term_input_id')
	for option in el.find_elements_by_tag_name('option'):
		if option.text == 'Spring 2013 Semester':
			option.click()

	driver.find_element_by_xpath("//input[@value='Submit']").click()
	# Wait for page
	time.sleep(wait_low)
	cid = driver.find_element_by_id("crn_id")
	cid.send_keys(ids)

	driver.find_element_by_xpath("//input[@value='Submit']").click()
	with open(path + sem_hash[sem] + "/" + ids, "w") as fn:
		print driver.page_source
		fn.write(BeautifulSoup(driver.page_source))
	time.sleep(wait_low)
	#driver.find_element_by_xpath("//td[@class='ntdefault']/a").click()
	driver.close()
	exit(0)

if __name__ == '__main__':
	ids = str(sys.argv[1])
	sem = str(sys.argv[2])
	if sem not in sem_hash:
		print "Could not find", sem, " semester"
		exit(1)
	my_test(ids, sem)