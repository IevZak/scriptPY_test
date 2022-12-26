from datetime import date, timedelta
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome, Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logger

url = "http://computer-database.gatling.io/computers"
date_test1 = str(date.today() - timedelta(days=3650))
date_now = str(date.today())
name = "Test_Eu" + str(time.time())
opts = ChromeOptions()
opts.add_experimental_option("detach", True)
serv_Obj = Service("/usr/bin/chromedriver")
companyNameID = 1

try:
    # precondition for Chrome
    opts.add_argument("start-maximized")
    opts.add_argument("--auto-open-devtools-for-tabs")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)

    # open Chrome
    driver = webdriver.Chrome(service=serv_Obj, options=opts)
    driver.get(url)

    # select and movie
    driver.find_element(By.ID, "add").click()
    driver.find_element(By.ID, "name").send_keys(name)
    driver.find_element(By.ID, "introduced").send_keys(date_test1)
    driver.find_element(By.ID, "discontinued").send_keys(date_now)

    # open list of company and choice company at name
    x = driver.find_element(By.ID, "company")
    drop = Select(x)
    drop.select_by_visible_text("RCA")

    # click button
    el = driver.find_element(By.XPATH, '//*[@class="btn primary"]')
    driver.execute_script("arguments[0].click();", el)

    # check result. search name new computer
    driver.find_element(By.ID, "searchbox").send_keys(name)
    driver.find_element(By.ID, "searchsubmit").click()

    # check Negative response
    # driver.find_element(By.XPATH, '//*[@class="well"]')
    if driver.find_element(By.XPATH, '//*[contains(text(),  "Nothing to display")]'):
        print("Test Failed. The new computer has not been added")
        logger.add_response("Test Failed. The new computer has not been added", str(url))
    else:
        print("Test passed. The new computer has not been added")

    # open DevTools
    # select = Service(driver.find_element_by_css_selector("select"))
    # driver.find_element(By.CSS_SELECTOR("body")).send_keys(Keys.F12)

    # driver.find_element(By.NAME, "Create this computer").click()
    # driver.find_element(By.XPATH("//*[local-name()='option' and text()='RCA']")).click()
    # # companyName = driver.find_element("//*[local-name() = 'option' and contains(@value, '1') and text() = 'Apple Inc.' ]"))
    # companyName = driver.find_element(By.XPATH('//*[local-name()="option"and contains(@value, "1")and text()="Apple Inc."]'))
    # companyName.click()

except Exception as ex:
    print(ex)
finally:
    time.sleep(15)
    driver.close()
    driver.quit()
