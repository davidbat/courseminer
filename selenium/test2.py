#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get('https://myneu.neu.edu/')
assert "myNEU" in driver.title
user = driver.find_element_by_name("user")
user.send_keys("batelu.d")
passw = driver.find_element_by_name("pass")
passw.send_keys("floorPOD")
driver.find_element_by_xpath("//input[@value='Login']").click()
# Wait for page
time.sleep(2)
driver.find_element_by_xpath("//div[@class='taboff']").click()
driver.find_element_by_xpath("(//span[@id='p_chan_text']/p/a/b)[3]").click()
# waitForPopUp
time.sleep(2)
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
driver.page_source

driver.find_element_by_xpath("//td[@class='ntdefault']/a").click()