
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
from twocaptcha import TwoCaptcha
import undetected_chromedriver as uc
import time
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument('--ignore-certificate-errors')


driver = uc.Chrome(headless=False, options=chrome_options)

url = 'https://nowsecure.nl/'
driver.get(url)
time.sleep(10)
driver.execute_script(f"window.open('{url}', '_blank')")
input()