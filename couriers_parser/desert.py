from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import time

def parse_d():   

  chrome_options = Options()
  chrome_options.add_argument("--auto-open-devtools-for-tabs")
  driver = uc.Chrome(headless=False, options=chrome_options)
  data = []
  try:
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument('--ignore-certificate-errors')
    data = []
    url = 'https://desertgun.club/stuffer/login.php'
    driver.get(url)
    time.sleep(10)
    driver.execute_script(f"window.open('{url}', '_blank')")
    time.sleep(15)
    driver.refresh()
    time.sleep(15)
    print(driver.page_source)
    login = WebDriverWait(driver, 15).until(
      EC.presence_of_element_located((By.NAME, 'login'))
    )
    password = WebDriverWait(driver, 15).until(
      EC.presence_of_element_located((By.NAME, 'password'))
      )
    submit = WebDriverWait(driver, 15).until(
      EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
      )
    login.send_keys('lucianovivaldi') 
    password.send_keys('BVPmhE864Af')
    submit.click()

    sleep(2)
    driver.get('https://desertgun.club/stuffer/drops.php')
    table = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, 'new-couriers-table'))
    )
    trs = WebDriverWait(table, 10).until(
      EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
      )
    print(len(trs))
    for tr in trs[1:]:
      tds = tr.find_elements(By.TAG_NAME, 'td')
      row_text = [x.text for x in tds]
      if len(row_text) < 8: continue 
      data.append({
          "city": row_text[3],
          "state": row_text[4],
          "zip_code": row_text[5],  # int(get_numbers(zip_code)),
          "status": row_text[6],
          "expired": row_text[7],
          "website": 'AMG STUFF [Franklin]'
      })


  except Exception as e:
    print(e)
  finally:
    driver.quit()
    return data

print(parse_d())