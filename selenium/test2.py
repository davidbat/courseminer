#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import time 
wait_time = 3
fp = webdriver.FirefoxProfile()
fp.set_preference('browser.sessionstore.postdata', 1)
#fp = webdriver.FirefoxProfile('/home/dave/.mozilla/firefox/yoijpybx.default/')

driver = webdriver.Firefox(fp)

def my_test():
	
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
	time.sleep(2)
	cid = driver.find_element_by_id("crn_id")
	cid.send_keys("36228")

	driver.find_element_by_xpath("//input[@value='Submit']").click()
	print driver.page_source
	time.sleep(3)
	driver.find_element_by_xpath("//td[@class='ntdefault']/a").click()


if __name__ == '__main__':
	my_test()