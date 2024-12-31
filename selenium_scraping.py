from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


driver = webdriver.Firefox()
driver.get("https://www.reddit.com")

# id = main-content

elem = driver.find_element(By.NAME, "q")

elem.clear()
elem.send_keys("Machine learning news")
elem.send_keys(Keys.ENTER)

driver.close()