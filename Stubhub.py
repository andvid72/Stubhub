from seleniumwire import webdriver
# import undetected_chromedriver as webdriver
# import nodriver as webdriver
# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Stubhub_Module import get_seats
import csv,time

#Inicia Driver
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options = options)

#Va a la web a scrapear
url = "https://www.stubhub.com/us-open-tennis-flushing-tickets-8-30-2024/event/152504282"
driver.get(url)

# 2 tickets
try: 
	path = '//*[@id="modal-root"]/div/div/div/div[2]/div[3]/button'
	elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, path)))
	driver.find_element(By.XPATH, path).click()
except: pass

# elije USD
try: 
	path = '//*[@id="event-detail-header"]/div/div/div[2]/div/div[1]/div[1]/div'
	elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, path)))
	driver.find_element(By.XPATH, path).click()
	time.sleep(10)
except: pass
try: 
	path = '//*[@id="event-detail-header"]/div/div/div[2]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/select/option[46]'
	elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, path)))
	driver.find_element(By.XPATH, path).click()
	time.sleep(10)
except: pass
try: 
	path = '//*[@id="event-detail-header"]/div/div/div[2]/div/div[1]/div[2]/div/div/div[3]/button'
	elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, path)))
	driver.find_element(By.XPATH, path).click()
	time.sleep(2)
except: pass

# Scroll
driver.execute_script("document.body.style.zoom = '0.5'")
list_seats = [['Section','Row','Price','Score']]
stacker = 0; scroll_counter = 0
for x in range(40):	
	elem = driver.find_element(By.XPATH, '//*[@id="listings-container"]')
	html_content = elem.get_attribute('outerHTML')
	prev_stacker = stacker
	list_seats,stacker = get_seats(html_content,list_seats,stacker)
	if prev_stacker == stacker: 
		scroll_counter += 1
		if scroll_counter == 3:	break
	else: scroll_counter = 0
	scroll_elem = driver.find_element(By.XPATH, '//*[@id="stubhub-event-detail-listings-scroll-container"]')
	try: driver.execute_script("arguments[0].scrollBy(0,3000);",scroll_elem)
	except: pass
	time.sleep(2)

driver.quit()

# CSV
file_path = "C:/Users/Videla/Downloads/tickets.csv"
with open(file_path, 'w', newline='') as csvfile:
	csv_writer = csv.writer(csvfile)
	csv_writer.writerows(list_seats)