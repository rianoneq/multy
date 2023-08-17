
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
from twocaptcha import TwoCaptcha

import undetected_chromedriver as uc

driver = uc.Chrome(headless=True)
couriers = []
try:
  driver.get('https://goodygoods.services.st/login/')
  username = WebDriverWait(driver, 15).until(
      EC.presence_of_element_located((By.NAME, 'username'))
  )
  password = WebDriverWait(driver, 15).until(
      EC.presence_of_element_located((By.NAME, 'password'))
  )
  submit = WebDriverWait(driver, 15).until(
      EC.presence_of_element_located((By.CLASS_NAME, 'btn-block'))
  )
  username.send_keys("nordioo")
  password.send_keys("J69KRXbymj")
  submit.click()


  driver.get('https://goodygoods.services.st/courier_request/')
  table = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, 'main_table'))
  )
  rows = [row.text.strip() for row in table.find_elements(By.TAG_NAME, 'tr')]
  for row in rows:
    row = row.split(', ')
    if len(row)>2:
      last = row[-1].split('\n')[-1].split(' ')
      if len(last) > 1:
        expired = last[-1]
      else:
        expired = 'n/a'
      status = last[0]

      couriers.append({
        'city': row[0],
        'state': row[1],
        'zip_code': row[2],
        'status': status,
        'expired': expired,
        'website': 'Goody Goods [Dee_Kline]'
      })
finally: 
  driver.close()
  driver.quit()
print(couriers)