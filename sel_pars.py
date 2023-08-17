# -*- coding: utf8 -*-
import datetime
from lib2to3.pgen2 import driver
import random
import re
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class parse_unick_cases:
  def __init__(self, url, rows, driver, service):
    self.url = url
    self.rows = rows
    self.driver = driver
    self.service = service
  
  def parse_data_housecargo(self):
      
      data = []

      for tr in self.rows:
        tds = WebDriverWait(tr, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
        )
        
        full_adress = tds[3].text.split('|')

        city = full_adress[1].strip()
        zip_index = full_adress[2].strip()
        reg = full_adress[3].strip()
        expired = tds[10].text.strip()
        status = tds[4].text.strip()

        data.append(
            {'city': city,
            'state': reg,
            'zip_code': zip_index,
            'status': status,
            'expired': expired,
            'website': self.service}
        )

      return data 

  def parse_data_arena(self):

      data = []

      for tr in self.rows:
        tds = WebDriverWait(tr, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
        )

        status_and_exp = tds[5].text.split()

        print([td.text for td in tds])
        city = tds[2].text.strip()
        region = tds[3].text.strip()
        zip_index = tds[4].text.strip()
        expired = status_and_exp[1].strip() if len(status_and_exp) < 3 else ' '.join(status_and_exp[1:])
        status = status_and_exp[0].strip() 


        data.append(
            {'city': city,
            'state': region,
            'zip_code': zip_index,
            'status': status,
            'expired': expired,
            'website': self.service}
        )


      return data
  
  def parse_data_185(self):
      
      data = [] 
      tds2 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'assign-courier-select'))
        )
      options = WebDriverWait(tds2, 10).until(
          EC.presence_of_all_elements_located((By.TAG_NAME, 'option'))
      )

      for tr in self.rows:
        tds = WebDriverWait(tr, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
        )

        city_and_state = tds[3].text.split('\n')

        city_and_zip = city_and_state[1].split(',')
        city = city_and_zip[0].strip() 
        state = city.split()[-1]
        city = city.replace(state, '').strip()
        zip_index = city_and_zip[1].strip()
        status = tds[5].text.strip() 
        expired = tds[7].text.strip() 


        data.append(
            {'city': city,
            'state': state,
            'zip_code': zip_index,
            'status': status,
            'expired': expired,
            'website': self.service}
        )
      for option in options:
        

        data_ = option.text.split('/')
        #print(data)
        state = data_[1].strip()
        city = data_[0].strip()
        zip_index = data_[2].split('-')[0].strip()
        status = data_[2].split('(exp:')[0].strip().replace(f'{zip_index} - ', '')
        expired = data_[2].split('(exp:')[1].strip().replace(')', '') 
        expired = 'n/a' if expired == 'n' else expired 


        data.append(
            {'city': city,
            'state': state,
            'zip_code': zip_index,
            'status': status,
            'expired': expired,
            'website': self.service}
        )
        

      return data
  
  def parse_data_droid(self):
      
      data = []

      for tr in self.rows:
        tds = WebDriverWait(tr, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
        )
        
        full_adress = tds[2].text.split('|')

        city = full_adress[-3].strip()
        zip_index = full_adress[-1].strip()
        state = full_adress[-2].strip()
        expired_date = tds[3].text.strip().split()
        expired = f'{expired_date[-3]} {expired_date[-2]}'
        status = tds[5].text.strip()

        data.append(
            {'city': city,
            'state': state,
            'zip_code': zip_index,
            'status': status,
            'expired': expired,
            'website': self.service}
        )

      #print(data)
      return data 
  
  def parse_data_admwest(self):
      
      data = []

      for tr in self.rows:
        tds = WebDriverWait(tr, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
        )
        
        city = tds[8].text.strip()
        state = tds[9].text.strip()
        zip_index = tds[10].text.strip()
        status = tds[11].text.strip()
        expired = tds[12].text.strip()

        data.append(
            {'city': city,
            'state': state,
            'zip_code': zip_index,
            'status': status,
            'expired': expired,
            'website': self.service}
        )

      return data 
  
  def parse_data_arsenal(self):
      
      data = []

      for tr in self.rows:
        tds = WebDriverWait(tr, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
        )
        
        city = 'n/a'
        state = tds[1].text.strip()
        zip_index = tds[2].text.strip()
        status = tds[3].text.strip()
        expired = tds[4].text.strip() if tds[4].text.strip() != '' else 'n/a'

        data.append(
            {'city': city,
            'state': state,
            'zip_code': zip_index,
            'status': status,
            'expired': expired,
            'website': self.service}
        )

      return data 
  
  def parse_data_gonzaproject(self):
      
      data = []

      for tr in self.rows:
        tds = WebDriverWait(tr, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
        )
        
        city = 'n/a'
        state = tds[1].text.strip()
        zip_index = tds[2].text.strip()
        status = tds[3].text.strip()
        expired = tds[4].text.strip().split('\n')[0] if tds[4].text.strip() != '' else 'n/a'

        data.append(
            {'city': city,
            'state': state,
            'zip_code': zip_index,
            'status': status,
            'expired': expired,
            'website': self.service}
        )

      return data 
  
  def parse_data_cbpanel(self):
    
    data = [] 

    for tr in self.rows:
      tds = WebDriverWait(tr, 10).until(
          EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
      )

      city_and_state = tds[3].text.split('\n')

      state = re.findall(r'[A-Z]{2,}', ''.join(tds[3].text))[0]
      city_and_zip = city_and_state[1].replace(state, '').split(',')
      city = city_and_zip[0].strip()
      zip_index = city_and_zip[1].strip()
      status = tds[6].text.strip() 
      expired = tds[8].text.strip() 


      data.append(
          {'city': city,
          'state': state,
          'zip_code': zip_index,
          'status': status,
          'expired': expired,
          'website': self.service}
      )

    return data
  
  def parse_data_193(self):
    
    data = [] 

    for i in self.rows:
      row_text = [x.text.strip() for x in i.find_elements_by_tag_name('td')]
      full_adress = row_text[3].split('\n')
      full_adress = full_adress[1].split(',')
      city = full_adress[0].split()[0]
      state = full_adress[0].split()[1]

      zip_index = full_adress[-2].strip().split(',')[0]
      

      couriers_data = {
                  "city": city,
                  "state": state, 
                  "zip_code": zip_index,  # int(get_numbers(zip_code)),
                  "status": row_text[6],
                  "expired": row_text[7] if row_text[7] != '' else 'n/a',
                  "website": self.service
              }
      data.append(couriers_data)
    return data



  def parse(self):
    if 'housecargo.ru' in self.url:
      data = self.parse_data_housecargo()
    elif '31337.arenaproject.family' in self.url:
      data = self.parse_data_arena()
    elif '185.43.7.183' in self.url:
      data = self.parse_data_185()
    elif 'droid-club.com' in self.url:
      data = self.parse_data_droid()
    elif 'admwest.com' in self.url:
      data = self.parse_data_admwest()
    elif 'arsenal.st' in self.url:
      data = self.parse_data_arsenal()
    elif 'gonzaproject.biz' in self.url:
      data = self.parse_data_gonzaproject()
    elif 'cbpanel.ws' in self.url:
      data = self.parse_data_cbpanel()
    elif '193.37.212.30' in self.url:
      data = self.parse_data_193()
    elif 'staffer.adminpanel' in self.url:
      data = self.staffer_adminpanel()

      
    #print(data)
    return data

class phantom_scrapper:
  def __init__(self, url_login, data_page_url, username, passw, service):
    self.driver = self.configurate_driver()

    self.url_login = url_login
    self.data_page_url = data_page_url
    self.username = username
    self.passw = passw
    self.service = service

  def configurate_driver(self):

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920,1080")
    self.driver = webdriver.Chrome(r'chromedriver.exe', options=chrome_options)

    return self.driver

  def login(self):
    print(f'logging.. site: {self.url_login}')
    try:
      self.driver.get(self.url_login)
      
      inputs = WebDriverWait(self.driver, 10).until(
          EC.presence_of_all_elements_located((By.TAG_NAME, 'input'))
      )
      login_url = self.driver.current_url

      try:
        buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))
        )
        #print(len(buttons))
        button = buttons[-1]
        
      except:
        try:

          button = buttons[-2]
        except:
          for i in inputs:
            if i.get_attribute('type') == 'submit':

              button = inputs[inputs.index(i)]
          
      for i in inputs: 
        if i.get_attribute('type') == 'text':
          user_input = inputs[inputs.index(i)]
        elif i.get_attribute('type') == 'password':
          passw_input = inputs[inputs.index(i)]

      ActionChains(self.driver).move_to_element(user_input).click(user_input).perform()
      sleep(.3)
      
      user_input.send_keys(self.username)
      sleep(.5)
      ActionChains(self.driver).move_to_element(passw_input).click(passw_input).perform()
      sleep(.25)
      passw_input.send_keys(self.passw)
      sleep(.10)
      #button.click()
      ActionChains(self.driver).move_to_element(button).click(button).perform()
      sleep(1.5)
      if self.driver.current_url == login_url:
        raise Exception
      print('logged sussessfully!')
    except Exception as e:
      print(f'ERR0R: {e}')
      return

  def get_data_rows(self):
    
    self.driver.get(self.data_page_url)
    
    try:
      data_table = WebDriverWait(self.driver, 10).until(
          EC.presence_of_element_located((By.TAG_NAME, 'tbody'))
      )

      trs = WebDriverWait(data_table, 10).until(
          EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
      )
    except:
      return []

    return trs 

  def main(self):
    try:
      self.login()

      sleep(.4)
      rows = self.get_data_rows()
      parse = parse_unick_cases(url=self.data_page_url,
                                rows=rows,
                                driver=self.driver,
                                service=self.service)
      return parse.parse()
    except Exception as e:
      print(e, self.data_page_url)
    finally:
      self.driver.close()
      self.driver.quit()

# scrapper = phantom_scrapper(url_login='http://stuffer.admwest.com/site/login',
#                             username='luciano',
#                             passw='V1valD1',
#                             data_page_url='http://stuffer.admwest.com/drop/index',
#                             service='Leon656').main()

# scrapper = phantom_scrapper(url_login='http://housecargo.ru/#/couriers',
#                             username='lucianovivaldi',
#                             passw='BVPmhE864Ar',
#                             data_page_url='http://housecargo.ru/#/couriers',
#                             service='Reinhardt Drops').main()
   
# print(scrapper)
# scrapper = phantom_scrapper(url_login='http://185.43.7.183/stuffer/login.php',
#                             username='lucianovivaldi',
#                             passw='BVPmhE864Am',
#                             data_page_url='http://185.43.7.183/stuffer/drops.php',
#                             service='USA дроп-сервис LEON [SEPTEMBER]').main()
# print(scrapper)
# scrapper = phantom_scrapper(url_login='https://goodygoods.services.st/login/',
#                             username='nordioo',
#                             passw='J69KRXbymj',
#                             data_page_url='https://goodygoods.services.st/courier_request/',
#                             service='Goody Goods [Dee_Kline]ч').main()
# print(scrapper)
# scrapper = phantom_scrapper(data_page_url='http://193.37.212.30/stuffer/drops.php', 
#                              url_login='http://193.37.212.30/stuffer/login.php',
#                              username='MrBugsBunny',
#                              passw='MrBugsBunny28',
#                              service='fastpack [Docent]').main()

# scrapper = phantom_scrapper(data_page_url='http://gonzaproject.biz/drop_request', 
#                              url_login='https://gonzaproject.biz/login',
#                              username='MrBugsBunny',
#                              passw='BVPmhE864cg',
#                              service='Gonza Project').main()
# print(scrapper)

