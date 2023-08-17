# -*- coding: utf8 -*-
from cmath import log
import requests
from fake_useragent import UserAgent 
import json
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import time

class parse_google:
  def __init__(self, url, service):
      self.url = url
      self.service = service
      self.sheet_id = '1IJbvHkorp2WwkLDsBr0eosgc29mnLLr_WVpnSYq-Eqw'
      self.sheet_id2 = '1IJbvHkorp2WwkLDsBr0eosgc29mnLLr_WVpnSYq-Eqw'
      self.api_key = 'AIzaSyCSCTRGPKqbkGh3IV2ZCosDrsjzHqMpSgE'
  
  def main(self):

    data = []

    sheet_data = requests.get(f"""
      https://sheets.googleapis.com/v4/spreadsheets/{self.sheet_id}/values/Доп адреса!B1:K28?key={self.api_key}
    """).text

    r = json.loads(sheet_data)

    for i in r['values'][3:]:
      if i[0] == '':
        break
      data_ = i[0].split('\n')
      d = data_[1].split(' ')
      if len(i) == 1: continue
      zip_code = d[-2].strip()
      state = d[-1].strip() if d[-1].strip() else 'n/a'
      city = ' '.join(d).replace(f' {zip_code} {state}', '').strip() if ' '.join(d).replace(f' {zip_code} {state}', '').strip() else 'n/a'
      status = i[-2].strip() if i[-2].strip() else 'n/a'
      expired = i[-1].strip().replace('До ', '').replace('\t','') if i[-1].strip() != '' else 'n/a'

      data.append(
            {'city': city,
            'state': state,
            'zip_code': zip_code,
            'status': status,
            'expired': expired,
            'website': self.service}
        )
    sheet_data2 = requests.get(f"""
        https://sheets.googleapis.com/v4/spreadsheets/{self.sheet_id}/values/Адреса!C1:L28?key={self.api_key}
      """).text

    r = json.loads(sheet_data2)
    for i in r['values'][4:]:
      if len(i) == 1: break
      if len(i) < 2: continue
      if i[0] == '': continue
      data_ = i[0].split('\n')
      d = data_[1].split(' ')
      if len(d) < 3: continue
      zip_code = d[-2].strip() if d[-2] else 'n/a'
      state = d[-1] if d[-1] else 'n/a'
      city = ' '.join(d).replace(f'{zip_code} {state}', '').strip() if ''.join(d).replace(f'{zip_code}{state}', '').strip() else 'n/a'
      # d = data_[1].split(',')
      # zip_code = d[1].strip()
      # state = d[0].split(' ')[-1].strip() if d[0].split(' ')[-1].strip() else 'n/a'
      # city = d[0].replace(f' {state} ', '').strip() if d[0].replace(f' {state} ', '').strip() else 'n/a'
      status = i[-2].strip()
      expired = i[-1].strip().replace('До ', '') if i[-1].strip() != '' else 'n/a'

      data.append(
            {'city': city,
            'state': state,
            'zip_code': zip_code,
            'status': status,
            'expired': expired,
            'website': self.service}
        )

    return data
  
class parse_hr:
  def __init__(self, parse_url, service):
      self.parse_url = parse_url
      self.service = service
      self.headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
      'Authorization': 'Basic ZHBuaW1kYTpkb0BvWDNhaGVpY2U=',
      'Connection': 'keep-alive',
      'Cookie': 'laravel_session=eyJpdiI6ImE0YXRrMFRpdVg3UGVoT0pTZmJKS3c9PSIsInZhbHVlIjoiQlhlQWpXUTBKcEtvY2dMNk5GcDhWUXlMdzhrS21BeHVubUE5TTV3dll1XC9XcEFFK2EyOG5ET0RrTXVwWkwyd0NIcWYxQUdPM3ZcL2FJQXBPUm5tODhhUT09IiwibWFjIjoiMGE4OTE5YzcyNmU3MWJmZTgwZjI0ZTU0ODU3MmYxMTg2ZjkxZjIzMzk1MzBhNGIxY2JkYTQ2ZWEzNjNlMzNkNSJ9',
      'Referer': 'http://staffer.hr-solutions.space/login',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'}
  
  def parse_hr_(self):
    
    session = requests.Session()
    r = session.get('http://staffer.hr-solutions.space/login', headers={'Authorization': 'Basic ZHBuaW1kYTpkb0BvWDNhaGVpY2U='})
    payload = {
      'login': 'lucianovivaldi2',
      'password': 'lucianovivaldi2'
    }
    parse_page = session.post('http://staffer.hr-solutions.space/login', json=payload, headers={'Authorization': 'Basic ZHBuaW1kYTpkb0BvWDNhaGVpY2U=', 'Referer': 'http://staffer.hr-solutions.space/login'})
    # print(parse_page.text)
    z = session.get('http://staffer.hr-solutions.space/reshippers', headers={'Authorization': 'Basic ZHBuaW1kYTpkb0BvWDNhaGVpY2U=', 'Referer': 'http://staffer.hr-solutions.space/login'})
    req = BeautifulSoup(z.text, 'html.parser')
    # print(req)
    alerts = req.find_all('input', {'name': 'alert_id'})
    for alert in alerts:
      payload = {'alert_id': alert['value']}
      session.post('http://staffer.hr-solutions.space/alerts', json=payload, headers={'Authorization': 'Basic ZHBuaW1kYTpkb0BvWDNhaGVpY2U='})
    data = []
    r = session.get('http://staffer.hr-solutions.space/reshippers', headers={'Authorization': 'Basic ZHBuaW1kYTpkb0BvWDNhaGVpY2U='})
    soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup)
    tb = soup.find('tbody')
    #print(tb)
    for i in tb.find_all('tr'):
        row_text = [x.text for x in i.find_all('td')]
        data.append({
            "city": row_text[6],
            "state": row_text[7],
            "zip_code": row_text[8],  # int(get_numbers(zip_code)),
            "status": row_text[3],
            "expired": row_text[10].replace('\n', '').replace('\t','').strip(),
            "website": self.service
        })
    return data

# """селениумом не парсится, переделал на реквестах"""
class parse_unick_cases:
  def __init__(self, parse_url, username, passw, login_url, service):
    self.parse_url = parse_url
    self.passw = passw
    self.username = username
    self.login_url = login_url
    self.service = service


  def login_goodygoods(self):
    try:
      self.driver.get(self.login_url)
      
      inputs = WebDriverWait(self.driver, 10).until(
          EC.presence_of_all_elements_located((By.TAG_NAME, 'input'))
      )
      login_url = self.driver.current_url

      buttons = WebDriverWait(self.driver, 10).until(
          EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))
      )
      button = buttons[-2]
        
          
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

  def parse_goodygoods(self):
    self.driver.get(self.parse_url)
    data = [] 
    data_table = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'main_table'))
    )
    tbody = WebDriverWait(data_table, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'tbody'))
    )
    trs = WebDriverWait(tbody, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
    )
    for tr in trs:
      tds = WebDriverWait(tr, 10).until(
          EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
      )
     # print(tr.text)
      full_adress = tds[1].text.split(',')

      if 'United States' in ''.join(full_adress):
        state = full_adress[1].strip()
        city = full_adress[0].strip()
        zip_index = full_adress[2].strip()
        status = tds[2].text.strip() 
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

  def parse_tortuga(self):
    self.driver.get(self.parse_url)
    #print(self.parse_url, self.driver.current_url)
    html = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'html'))
    )
    html.send_keys(Keys.END)   
    sleep(5)
    data_table = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'data-table-couriers'))
    )
    # print(data_table.text)
    tbody = WebDriverWait(data_table, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'tbody'))
    )[0]
    trs = WebDriverWait(tbody, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
    )
    data = [] 

    for tr in trs:
      tds = WebDriverWait(tr, 10).until(
          EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
      )


      state = tds[5].text.strip()
      city = tds[4].text.strip()
      zip_index = tds[6].text.strip()
      status = tds[-1].text.strip().split('\n')[0]
      expired = tds[-4].text.strip().split('\n')[0]


      data.append(
          {'city': city,
          'state': state,
          'zip_code': zip_index,
          'status': status,
          'expired': expired,
          'website': self.service}
      )

    return data

  def login_tortuga(self):
    self.driver.get(self.login_url)

    inputs = WebDriverWait(self.driver, 10).until(
      EC.presence_of_all_elements_located((By.TAG_NAME, 'input'))
    )
    login_url = self.driver.current_url

    try:

      try:
        buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))
        )
        
        button = buttons[-1]
      except:
        for i in inputs:
          if i.get_attribute('type') == 'submit':

            button = inputs[inputs.index(i)]
          
      checkbox = False
      for i in inputs: 
        if i.get_attribute('type') == 'text':
          user_input = inputs[inputs.index(i)]
        elif i.get_attribute('type') == 'password':
          passw_input = inputs[inputs.index(i)]
        elif i.get_attribute('type') == 'checkbox':
          checkbox = inputs[inputs.index(i)]

      ActionChains(self.driver).move_to_element(user_input).click(user_input).perform()
      sleep(.3)
      
      user_input.send_keys(self.username)
      sleep(.5)
      ActionChains(self.driver).move_to_element(passw_input).click(passw_input).perform()
      sleep(.25)
      passw_input.send_keys(self.passw)
      sleep(.10)
      ActionChains(self.driver).move_to_element(checkbox).click(checkbox).move_to_element(button).click(button).perform()

      sleep(1.5)
      if self.driver.current_url == login_url:
        raise Exception
      print('logged sussessfully!')
    except Exception as e:
      print(f'ERR0R: {e}')

  def parse_sbx(self):
    self.driver.get(self.parse_url)
    #print(self.parse_url, self.driver.current_url)

    
    data_table = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'rounded-corner'))
    )
    # print(data_table.text)
    tbody = WebDriverWait(data_table, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'tbody'))
    )[0]
    trs = WebDriverWait(tbody, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
    )[3:]
    data = [] 

    for tr in trs:
      tds = WebDriverWait(tr, 10).until(
          EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
      )
      full_text = [x.text for x in tds]
      #print(full_text)

      adress = full_text[1].split(',')
      status_and_exp = full_text[2].split('\n')
      state = adress[0].strip()
      city = adress[1].strip()
      zip_index = adress[2].strip()
      status = status_and_exp[0]
      expired = status_and_exp[1]


      data.append(
          {'city': city,
          'state': state,
          'zip_code': zip_index,
          'status': status,
          'expired': expired,
          'website': self.service}
      )

    return data

  def login_sbx(self):
    self.driver.get(self.login_url)

    inputs = WebDriverWait(self.driver, 10).until(
      EC.presence_of_all_elements_located((By.TAG_NAME, 'input'))
    )

    login_url = self.driver.current_url
    try:


      for i in inputs: 
        if i.get_attribute('type') == 'text':
          user_input = inputs[inputs.index(i)]
        elif i.get_attribute('type') == 'password':
          passw_input = inputs[inputs.index(i)]
        elif i.get_attribute('type') == 'image':
          button = inputs[inputs.index(i)]

      ActionChains(self.driver).move_to_element(user_input).click(user_input).perform()
      sleep(.3)
      
      user_input.send_keys(self.username)
      sleep(.5)
      ActionChains(self.driver).move_to_element(passw_input).click(passw_input).perform()
      sleep(.25)
      passw_input.send_keys(self.passw)
      sleep(.10)
      ActionChains(self.driver).move_to_element(button).click(button).perform()


      sleep(1.5)
      if self.driver.current_url == login_url:
        raise Exception
    except Exception as e:
      print(f'ERR0R: {e}')


  def login_staffer_adminpanel(self):
    self.driver.get(self.login_url)

    inputs = WebDriverWait(self.driver, 10).until(
      EC.presence_of_all_elements_located((By.TAG_NAME, 'input'))
    )

    login_url = self.driver.current_url
    try:


      for i in inputs: 
        if i.get_attribute('type') == 'text':
          user_input = inputs[inputs.index(i)]
        elif i.get_attribute('type') == 'password':
          passw_input = inputs[inputs.index(i)]
      
      button = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.ID, 'auth'))
    )
      ActionChains(self.driver).move_to_element(user_input).click(user_input).perform()
      sleep(.3)
      
      user_input.send_keys(self.username)
      sleep(.5)
      ActionChains(self.driver).move_to_element(passw_input).click(passw_input).perform()
      sleep(.25)
      passw_input.send_keys(self.passw)
      sleep(.10)
      ActionChains(self.driver).move_to_element(button).click(button).perform()

      sleep(1.5)
      if self.driver.current_url == login_url:
        raise Exception
      print('logged sussessfully!')
    except Exception as e:
      print(f'ERR0R: {e}')

  def parse_staffer_adminpanel(self):
    data = [] 

    statuses_by_colors = {
      'rgb(65, 119, 40) !important': 'Stable',
      'rgb(9, 210, 46) !important': 'Work',
      'rgb(238, 164, 13) !important': 'Test',
      'rgb(43, 216, 242) !important': 'Prolblem',
      'rgb(204, 51, 17) !important': 'Ripper',
      'rgb(22, 39, 204) !important': 'Finish',
    }
    
    self.driver.get(self.parse_url)

    for i in range(1, 100):
      sleep(3)
      paginate_menu = WebDriverWait(self.driver, 10).until(
          EC.presence_of_element_located((By.ID, 'paginator'))
        )
      paginate_btns = WebDriverWait(paginate_menu, 10).until(
          EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn-icon'))
        )
      # x = [x.text.strip() for x in paginate_btns]
      # print(x)

      
      sleep(3)
      data_table = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'mainTable'))
      )
      tbody = WebDriverWait(data_table, 10).until(
          EC.presence_of_all_elements_located((By.TAG_NAME, 'tbody'))
      )[0]
      trs = WebDriverWait(tbody, 10).until(
          EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
      )

      for tr in trs:
        tds = WebDriverWait(tr, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'td'))
        )
        span_with_styles = tds[2].find_elements_by_tag_name('span')[2]
        status = span_with_styles.get_attribute("style")
        status_clear = status.split(';')[0].replace('color: ','')
        status = statuses_by_colors[status_clear]

        full_text = [x.text for x in tds]
        
        state = full_text[5].strip()
        city = full_text[4].strip()
        zip_index = full_text[6].strip()
        expired = full_text[7].strip()
        
        data.append(
            {'city': city,
            'state': state,
            'zip_code': zip_index,
            'status': status,
            'expired': expired,
            'website': self.service}
        )
      #print(data)
      try:
        next_btn = WebDriverWait(paginate_menu, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'ki-bold-arrow-next'))
       )
        next_btn = next_btn.find_element_by_xpath('..')

      except:
        return data
      ActionChains(self.driver).move_to_element(next_btn).click(next_btn).perform()
    return data

  def parse_desertgun(self): ...

  def login_desertgun(self):
    try:
      chrome_options = Options()
      chrome_options.add_argument("--auto-open-devtools-for-tabs")
      driver = uc.Chrome(headless=True, options=chrome_options)

      driver.execute_script('''window.open("https://desertgun.club/stuffer/login.php","_blank");''') # open page in new tab
      time.sleep(4) # wait until page has loaded
      driver.switch_to.window(window_name=driver.window_handles[0])   # switch to first tab
      driver.close() # close first tab
      driver.switch_to.window(window_name=driver.window_handles[0] )  # switch back to new tab
      time.sleep(1.5)
      driver.get("https://google.com")
      time.sleep(1.5)
      driver.get("https://desertgun.club/stuffer/login.php") # this should pass cloudflare captchas now
      login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'login'))
       )
      password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'password'))
       )
      submit = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
       )
      login.send_keys('lucianovivaldi') 
      password.send_keys('BVPmhE864Af')
      submit.click()

      time.sleep(2)
      driver.get('https://desertgun.club/stuffer/drops.php')
      table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'new-couriers-table'))
      )
      trs = WebDriverWait(table, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
       )
      data = []
      print(len(trs))
      for tr in trs:
        row_text = [x.text for x in tr.find_elements('td')]
        print(row_text)
        data.append({
            "city": row_text[6],
            "state": row_text[7],
            "zip_code": row_text[8],  # int(get_numbers(zip_code)),
            "status": row_text[3],
            "expired": row_text[10].replace('\n', '').replace('\t','').strip(),
            "website": self.service
        })
      return data

    finally: 
      driver.close()
      driver.quit()

  def parse_goody(self):
    driver = uc.Chrome(headless=True)
    couriers = []
    try:
      driver.get(self.login_url)
      username = WebDriverWait(driver, 15).until(
          EC.presence_of_element_located((By.NAME, 'username'))
      )
      password = WebDriverWait(driver, 15).until(
          EC.presence_of_element_located((By.NAME, 'password'))
      )
      submit = WebDriverWait(driver, 15).until(
          EC.presence_of_element_located((By.CLASS_NAME, 'btn-block'))
      )
      username.send_keys(self.username)
      password.send_keys(self.passw)
      submit.click()


      driver.get(self.parse_url)
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
    return couriers

  def main(self):

      if 'tort.top' in self.login_url:
        self.login_tortuga()
        sleep(4)
        data = self.parse_tortuga()
      elif 'sbx.team' in self.login_url:
        self.login_sbx()
        sleep(4)
        data = self.parse_sbx()
    
      elif 'staffer.adminpanel' in self.login_url:
        self.login_staffer_adminpanel()
        sleep(4)
        data = self.parse_staffer_adminpanel()

      elif 'desertgun' in self.login_url:
        self.login_desertgun()
        sleep(5)
        data = self.parse_desertgun()

      elif 'goodygoods' in self.login_url:
        data = self.parse_goody()

      return data

    
p = parse_unick_cases(parse_url='https://desertgun.club/stuffer/drops.php',
                      passw='BVPmhE864Af',
                      username='lucianovivaldi',
                      login_url='https://desertgun.club/stuffer/login.php',
                      service='desert').main()
print(p)
# p = parse_unick_cases(parse_url='https://goodygoods.services.st/courier_request/',
#                       passw=' J69KRXbymj',
#                       username='nordioo',
#                       login_url='https://goodygoods.services.st/login/',
#                       service='Goody Goods [Dee_Kline]').main()
# print(p)
# p = parse_unick_cases(parse_url='https://tort.top/user/couriers/all',
#                       passw='uD8MRvnG!V',
#                       username='Luciano',
#                       login_url='https://tort.top/',
#                       service='tortuga [Calypso]').main()
# print(p)
# p = parse_unick_cases(parse_url='https://sbx.team/?a=drop',
#                       passw='43qkonr0PN',
#                       username='nordo',
#                       login_url='https://sbx.team/',
#                       service='StrongBox').main()
# print(p)
# scrapper = parse_unick_cases(login_url='https://staffer.adminpanel.digital/',
#                             username='lucianovivaldi2',
#                             passw='lucianovivaldi2',
#                             parse_url='https://staffer.adminpanel.digital/employees',
#                             service='MoHomax').main()
                            
# print(scrapper)
# scrapper = parse_hr(parse_url='http://staffer.hr-solutions.space/reshippers',
#                             service='HR').parse_hr_()
# print(scrapper)
# pg = parse_google('https://docs.google.com/spreadsheets/d/1IJbvHkorp2WwkLDsBr0eosgc29mnLLr_WVpnSYq-Eqw/edit#rangeid=194589493',
#   service='Esk0bar').main()
# print(pg)

# scrapper = parse_unick_cases(login_url='https://goodygoods.services.st/login/',
#                             username='nordioo',
#                             passw='J69KRXbymj',
#                             parse_url='https://goodygoods.services.st/courier_request/',
#                             service='Goody Goods [Dee_Kline]').main()
# print(scrapper)

