
import json
from time import sleep
import requests
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent 


""" 
    парсинг сайтов с 'уникальным' логином, везде свой подход, заключающийся в отправке пост
    запроса с определенными параметрами, уникальными для каждого сайта
"""
class post_req_parser:
    def __init__(self, first_url, login, password, parse_url, service):
        self.first_url=first_url
        self.login=login
        self.password=password
        self.url=first_url
        self.parse_url=parse_url
        self.service=service

    def parse_gonza(self, session):
        s = session.get(url=self.parse_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'})
        soup = BeautifulSoup(s.text, 'html.parser')
        data = []

        for tr in soup.find('tbody').find_all('tr'):
            tds = tr.find_all('td')
            
            city = 'n/a'
            state = tds[1].text.strip()
            zip_index = tds[2].text.strip()
            status = tds[3].text.strip()
            expired = tds[4].text.strip().split('\n')[0] if tds[4].text.strip() != '' else 'n/a'
            expired = re.findall(r'[\d]{2} \/ [\d]{2} \/ [\d]{4}', expired)[0]
            data.append({
                'city': city,
                'state': state,
                'zip_code': zip_index,
                'status': status,
                'expired': expired,
                'website': self.service}
            )

        return data 
    
    def parse_fastpack(self, session):
        s = session.get(url=self.parse_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'})
        soup = BeautifulSoup(s.text, 'html.parser')
        data = []

        for tr in soup.find('tbody').find_all('tr'):

          row_text = [x.text.strip() for x in tr.find_all('td')]
          full_adress = row_text[3].split('\n')
          #full_adress = full_adress[1].split(',')
          city = full_adress[1].strip()
          state = full_adress[2].replace(',', '').strip()
          zip_index = full_adress[-1].strip().split(',')[0]
          

          couriers_data = {
                      'city': city,
                      'state': state, 
                      'zip_code': zip_index,  # int(get_numbers(zip_code)),
                      'status': row_text[6],
                      'expired': row_text[7] if row_text[7] != '' else 'n/a',
                      'website': self.service
                  }
          data.append(couriers_data)
        return data
    
    def parse_arsenal(self, session):
      s = session.get(url=self.parse_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'})
      soup = BeautifulSoup(s.text, 'html.parser')
      data = []
      for tr in soup.find_all('table', {'class': 'mws-table'})[1].find_all('tr')[1:]:
        row_text = [x.text.strip() for x in tr.find_all('td')]
        city = 'n/a'
        state = row_text[1].strip()
        zip_index = row_text[2].strip()
        status = row_text[3].strip()
        expired = row_text[4].strip() if row_text[4].strip() != '' else 'n/a'

        data.append( {
            'city': city,
            'state': state,
            'zip_code': zip_index,
            'status': status,
            'expired': expired,
            'website': self.service}
        )

      return data 
    
    def parse_admwest(self, session):
      s = session.get(url=self.parse_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'})
      soup = BeautifulSoup(s.text, 'html.parser')
      data = []
      #print(soup)
      for tr in soup.find('tbody').find_all('tr'):
        row_text = [x.text.strip() for x in tr.find_all('td')]
        city = row_text[8].strip()
        state = row_text[9].strip()
        zip_index = row_text[10].strip()
        status = row_text[11].strip()
        expired = row_text[12].strip()

        data.append(
            {'city': city,
            'state': state,
            'zip_code': zip_index,
            'status': status,
            'expired': expired,
            'website': self.service}
        )

      return data 
 
    def parse_droid(self, session):
      s = session.get(url=self.parse_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'})
      soup = BeautifulSoup(s.text, 'html.parser')
      data = []
      #print(soup)
      for tr in soup.find('tbody').find_all('tr'):
        row_text = [x for x in tr.find_all('td')]
        full_adress = row_text[2].text.strip().split('|')
        
        city = full_adress[-3].strip().strip()
        zip_index = full_adress[-1].strip().strip()
        state = full_adress[-2].strip().strip()
        
        expired_date = str(row_text[3]).split('br')[1]
        expired = expired_date[2:-1]
        status = row_text[5].text.strip()

        data.append(
            {'city': city,
            'state': state,
            'zip_code': zip_index,
            'status': status,
            'expired': expired,
            'website': self.service}
        )

      return data 
 
    def parse_185(self, session):
      s = session.get(url=self.parse_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'})
      soup = BeautifulSoup(s.text, 'html.parser')
      data = []
      tds2 = soup.find('select', {'id': 'assign-courier-select'})
      
      options = tds2.find_all('option')

      for tr in soup.find('tbody').find_all('tr'):
        row_text = [x.text.strip() for x in tr.find_all('td')]
        
        if row_text[1] != '': 
          row_text = [x.text.strip() for x in tr.find_all('td')]
          full_adress = row_text[3].split('\n')
          #full_adress = full_adress[1].split(',')
          city = full_adress[1].strip()
          state = full_adress[2].replace(',', '').strip()
          zip_index = full_adress[-1].strip().split(',')[0] 


          data.append(
              {'city': city,
              'state': state,
              'zip_code': zip_index,
              'status': row_text[6],
              'expired': row_text[7] if row_text[7] != '' else 'n/a',
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
 
    def parse_arena(self, session):
      session = requests.session()
      s = session.get(url=self.first_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'})
      sleep(.65)
      s = session.get(url=self.parse_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'})
      soup = BeautifulSoup(s.text, 'html.parser')
      table = soup.find('table', {'id': 'html_table'})
      trs = table.find('tbody').find_all('tr')
      #print(len(trs))
      data = []
      #for tr in trs:
        #print(tr.find_all('td'))
      tds = trs[0].find_all('td')
      row_text = [x.text for x in trs[0].find_all('td')]
      #print(row_text)
      status_and_exp = row_text[5].split()

      # print(status_and_exp)
      all_data = row_text[2].strip()
      all_data = all_data.split('(0) GOODShiddenhidden')
      for item in all_data:
        state = re.findall(r'[A-Z]{2,}', item)[0]
        data_except_state = item.split(state)
        city = data_except_state[0].strip()

        zip_index = re.findall(r"\d{5}", data_except_state[1].strip())[0]
        # if ':' in data_except_state[-1]:
        #   data_except_state[-1] = data_except_state[-1].replace(':','') 
        
        clean_exp_and_status = data_except_state[-1].replace(zip_index, '').split(':')[0].strip().replace(':','')

        #print(clean_exp_and_status)
        if 'more than a week' in clean_exp_and_status:
          status = clean_exp_and_status.replace('more than a week', '')
          expired = 'more than a week'
        else:
          expired = re.findall(r'[\d]{4}\-[\d]{2}\-[\d]{2}|[\d]{2}\-[\d]{2}\-[\d]{4}', clean_exp_and_status)
          #print(expired)
          for i in range(0, len(expired)):
            #print(i, expired[i], clean_exp_and_status)
            clean_exp_and_status = clean_exp_and_status.replace(expired[i], '')
          status = clean_exp_and_status
          expired = expired[0] if len(expired) > 0 else ''
          

        data.append(
            {'city': city,
            'state': state,
            'zip_code': zip_index,
            'status': status,
            'expired': expired,
            'website': self.service}
        )


      return data

    def parse_housecargo(self, session, token):
      res = []
      data = {
        'page': '1',
        'per': '1000000',
        'desc': 'true',
        'sort': 'courierCreateDate',
        'list': 'true',
      }
      headers = {
        'Authorization': f'Bearer {token}',
      }
      req = session.get(self.parse_url, data=data, headers=headers)
      
      req = json.loads(req.text)
      for i in req['items']:

        res.append({
          'city': i['courierCity'],
          'state': i['courierState'],
          'zip_code': i['courierIndex'],
          'status': i['courierStatusName'],
          'expired': i['courierExpDate'].replace('T00:00:00+00:00',''),
          'website': self.service,

        })
      return res
    
    def parse_sbx(self, session):
      s = session.get(url=self.parse_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'}).text
      soup = BeautifulSoup(s)

      data_table = soup.find('table', {'id': 'rounded-corner'})
      #print(data_table.text)
      tbody = data_table.find_all('tbody')[0]
      trs = tbody.find_all('tr')[3:]
      data = [] 
      all_data = trs[0].text

      all_data = all_data.split('take courier')
      #print(all_data)
      for item in all_data:
        if item:
          state_and_city_and_all = item.split(',')
          status_and_exp_and_zip = item.replace(','.join(state_and_city_and_all[2:]), '')
          state = state_and_city_and_all[0].strip()
          city = state_and_city_and_all[1].strip()
          zip_index = re.findall(r"\d{5}", state_and_city_and_all[-1].strip())[0]
          status_and_exp = state_and_city_and_all[-1].replace(zip_index, '').strip()
          if 'more than a week' in status_and_exp and \
             'working' in status_and_exp:

            expired = 'more than a week'
            status = status_and_exp.replace(expired, '').strip()
          else:
            for exp in status_and_exp.split():
              if '.' in exp :
                expired = exp
              else:
                expired = 'n/a'
            status = 'not work'

          data.append(
              {'city': city,
              'state': state,
              'zip_code': zip_index,
              'status': status,
              'expired': expired,
              'website': self.service}
          )

      return data
        
    def parse_goodygoods(self, headers):
      session = requests.session()
      proxies = {
        "http": "http://ZHNmqt:JxPLBs@217.29.63.40:11170/"
      }
      s = session.get(self.parse_url, headers=headers, proxies=proxies)
      soup = BeautifulSoup(s.text, 'html.parser')

      data = []
      

      for tr in soup.find('tbody').find_all('tr'):
        row_text = [x.text.strip() for x in tr.find_all('td')]

        data_ = row_text[0].split(',')
        #full_adress = full_adress[1].split(',')
        city = data_[0].strip()
        # if len(data_) < 2:
        #   continue
        state = row_text[1].strip()
        zip_index = data_[2].strip()
        status = row_text[2].strip()
        expired = row_text[-2].strip()

        data.append(
            {'city': city,
            'state': state,
            'zip_code': zip_index,
            'status': status,
            'expired': expired if expired != '' else 'n/a',
            'website': self.service}
        )
      
      s = session.get('https://goodygoods.services.st/courier/', headers=headers, proxies=proxies)
      # soup = BeautifulSoup(s.text, 'html.parser')
      
      return data
    
    def parse_torutga(self, session, creds):
      res = []
      good_statuses = ['working', 'testing']#
      s = session.get(url=self.parse_url)
      soup = BeautifulSoup(s.text)
      token = creds['access_token']
      #print(creds['access_token'])     
      heads = {'Authorization':f'Bearer {token}'}
      data = {
        'limit': '1500',
        'offset': '0'
      }
      # print(session.post('https://api.tort.top/couriers/filter', headers={'Authorization':f'Bearer NDg3ZDI3MzlkMWFiMTk5YTMyMTNlY2E4ZTdiNGRiZWRjNjU3MWE3MDVlYTNjODBlNzMyNjk4NTBkZTMzNTI3OA'}).text)
      couriers = session.post('https://api.tort.top/couriers/filter', data=data, headers=heads).text
      couriers = json.loads(couriers)
      for courier in couriers['data']:
        #print(couriers)
        if courier['attributes']['status'] in good_statuses:
            res.append({
              'city': courier['attributes']['contact']['city'],
              'state': courier['attributes']['contact']['state'],
              'zip_code': courier['attributes']['contact']['zip'],
              'status': courier['attributes']['status'],
              'expired': courier['attributes']['checked_at'][0:10] if courier['attributes']['checked_at'] else 'n/a',
              'website': self.service})
      #print(res)
      return res
    
    def parse_monomah(self, session):
      res = []
      status_ids = {'stable': '3', 
                    'work': '2',
                    'test': '1'}
      for status_id in status_ids:
        data = {
          'fields[variable_date][working_till][param]': 'equal',
          'type': 'defaultFilterForm',
          'page': '1',
          'perPage': '300',
          'tableTab': 'employees',
          'quickswitch[status_id]': status_ids[status_id],
          'quickswitch[state_code]': 'all',
        }
        
        s = session.get(url=self.parse_url)
        #??????????????????????????????????????
        XSRF_TOKEN = session.get('https://staffer.adminpanel.digital/employees').cookies
        #?????????????????????????????????????? 
        csrf_token = BeautifulSoup(s.text, 'html.parser').find('meta', {'name': 'csrf-token'})['content']
        headers = {
          'XSRF-TOKEN': f'{XSRF_TOKEN}',
          'x-csrf-token': csrf_token,
        }

        req = session.post('https://staffer.adminpanel.digital/employees/filter', headers=headers, data=data)#
        #??????????????????????????????????????

        expired = re.findall(r'[\d]{2}\\/[\d]{2}\\/[\d]{4}', req.text)

        couriers = re.findall(r'(?<=copy-content d-none)([\s\S]+?)(?=\<)', req.text)
          #expired = re.findall(r'[\d]{2}\\/[\d]{2}\\/[\d]{4}', f.read())

        
        #print(couriers, expired, f'exp len:{len(expired)}', f'cour len:{len(couriers)}')
        for couriers_data, exp_data in zip(couriers, expired):
          data = couriers_data.split('Address: ')[1].replace('\\n', '')
          data = data.split(',')
          zip_index = data[3].strip()
          is_zip_correct = re.findall(r'[\d]{5,}',zip_index)
          if not is_zip_correct:
            state = data[-2].strip()
            zip_index = data[-1].strip()
            city = data[2].strip()
          else:
            city = data[1].strip()
            state = data[2].strip()


          status = status_id
          expired = exp_data.replace('\\','')
          res.append({
            'city': city,
            'state': state,
            'zip_code': zip_index,
            'status': status,
            'expired': expired,
            'website': self.service
          })

      
      return res    


    def parse_desert(self, headers, cookies, session, proxies):
      #print(headers,cookies,proxies)
      parse_page = session.get(self.parse_url, headers=headers, cookies=cookies,proxies=proxies)
      print(parse_page)
      soup = BeautifulSoup(parse_page.text, 'lxml')
      couriers = []
      for i in soup.select('tbody tr'):
          row_text = [x.text for x in i.find_all('td')]
          # print(row_text)
          if row_text[0] != '\n\n\n':
              city = row_text[3].strip()
              id = row_text[1]
              state = row_text[4].strip()
              zip_code = row_text[5]
              status = row_text[6]
              expired = row_text[7]
              couriers_data = {
                  "id": id,
                  "city": city,
                  "state": state if state != '' else 'n/a',
                  "zip_code": zip_code,  # int(get_numbers(zip_code)),
                  "status": status,
                  "expired": expired,
                  "website": self.service
              }
              couriers.append(couriers_data)

      # print(couriers)
      return couriers

    def log_in(self, login_name, password_name):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "ru,en;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            'Connection': 'keep-alive',
        }
        
        session = requests.session()

        #костыль но бля мне 30 сайтов разных парсить надо)
        
        
        if 'sbx.team' in self.first_url:
          data = {
            'a': 'login',
            login_name: self.login,
            'x': '19',
            'y': '19',
            password_name: self.password,
          }
          session.post(self.first_url, headers=headers, data=data, verify=False)
        elif 'tort.top' in self.first_url:
          grant_type = 'password'
          client_id = '1139360955_3tqljkv6n0o4gkow08kwwkcgwowwkk4cgsgs8cwcs448ksgc0c'
          client_secret = '4qadd5ay0juooccg0o4cg8ko4swwoskc0884ogs8cw4ggw88cw'
          data = {
            login_name: self.login,
            password_name: self.password,
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': client_secret
          }
          s = session.post(self.first_url, headers=headers, data=data, verify=False)
          creds = json.loads(s.text)
          return session, creds
        elif 'goodygoods' in self.first_url:
          #token = session.get(self.first_url).cookies['csrftoken']
          
          # data = {
          #   'csrfmiddlewaretoken': token,
          #   login_name: self.login,
          #   password_name: self.password,
          # }
          # s = session.post('https://goodygoods.services.st/login/', data=data, headers=headers)

          #s = session.get('https://goodygoods.services.st/courier_request/', headers=headers)
          return headers
        elif 'adminpanel' in self.first_url:
          data = {
            login_name: self.login,
            password_name: self.password,
            'tableTab': 'false',
          }
          s = session.post(self.first_url, headers=headers, data=data)
          #print(s.status_code, s.text)
          return session
        elif 'housecargo' in self.first_url:
          
          s = session.post(self.first_url, json={'password': 'BVPmhE864Ar', 'username': 'lucianovivaldi'})
          #print(s.text)
          token = json.loads(s.text)['token']
          #print(s.status_code, token)
          
          return session, token
        elif 'desertgun.club' in self.first_url:
          # cookie for 1 year, cloudflare bypass

          cookies = {
              'cf_clearance': '_upovsmo_8BJIEBzu_j2o1U2xjPtBSupJH8RX35RKk4-1665522516-0-150',
          }
          proxies = {
            "http": "http://yVu61c:azmmkh@217.29.63.202:12031/"
          }
          headers = {
              # Requests sorts cookies= alphabetically
              'authority': 'desertgun.club',
              'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
              'cache-control': 'max-age=0',
              # Requests sorts cookies= alphabetically
              'referer': 'https://desertgun.club/stuffer/login.php',
              'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
              'sec-ch-ua-mobile': '?0',
              'sec-ch-ua-platform': '"Windows"',
              'sec-fetch-dest': 'document',
              'sec-fetch-mode': 'navigate',
              'sec-fetch-site': 'same-origin',
              'sec-fetch-user': '?1',
              'upgrade-insecure-requests': '1',
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
          }
          #response = session.get('https://www.ip2location.com/demo', cookies=cookies, headers=headers, proxies=proxies)
          response = session.get(self.first_url, cookies=cookies, headers=headers, proxies=proxies)
          print(response.text)
          soup = BeautifulSoup(response.text, 'lxml')
          CSRFName = soup.find_all('input')[0]['value']
          CSRFToken = soup.find_all('input')[1]['value']

          data = {
              'CSRFName': CSRFName,
              'CSRFToken': CSRFToken,
              'login': 'lucianovivaldi',
              'password': 'BVPmhE864Af'
          }
          s = session.post(self.first_url, headers=headers, data=data, cookies=cookies, proxies=proxies)
          print(s.status_code)

          s = session.get(self.parse_url, headers=headers, cookies=cookies, proxies=proxies)
          print(s.status_code)

          return session, headers, cookies, proxies
        else:
          data = {
            login_name: self.login,
            password_name: self.password
          }
          session.post(self.first_url, headers=headers, data=data, verify=False)
        #print(self.url, data)
        return session
    
    def parse(self):

        if 'gonzaproject.biz' in self.first_url:
          session = self.log_in('login', 'password')
          couriers = self.parse_gonza(session=session)
          return couriers
        elif '193.37.212.30' in self.first_url:
          session = self.log_in('login', 'password')
          couriers = self.parse_fastpack(session=session)
          return couriers
        elif 'arsenal.st' in self.first_url:
          session = self.log_in('login', 'password')
          couriers = self.parse_arsenal(session=session)
          return couriers

        elif 'droid-club' in self.first_url:
          session = self.log_in('username', 'password')
          couriers = self.parse_droid(session=session)
          return couriers
        elif '185.43' in self.first_url:
          session = self.log_in('login', 'password')
          couriers = self.parse_185(session=session)
          return couriers
        elif 'arenaproject' in self.first_url:
          couriers = self.parse_arena('session)')
          return couriers
        elif 'sbx.team' in self.first_url:
          session = self.log_in('login', 'passw')
          couriers = self.parse_sbx(session=session)
          return couriers
        elif 'tort.top' in self.first_url:
          tort_data = self.log_in('username', 'password')
          session = tort_data[0]
          creds = tort_data[1]
          couriers = self.parse_torutga(session=session, creds=creds)
          return couriers
        elif 'staffer.adminpanel' in self.first_url:
          session = self.log_in('login', 'password')
          couriers = self.parse_monomah(session=session)
          return couriers
        
        # в пизду нахуй селениумом буду делать для него
        # а не все норм
        elif 'housecargo' in self.first_url:
          house_data = self.log_in('username', 'password')

          session = house_data[0]
          token = house_data[1]
          couriers = self.parse_housecargo(session=session, token=token)
          return couriers
        #тоже самое наверн
        elif 'goodygoods' in self.first_url:
          #headers = self.log_in('username', 'password')
          session_id = '72g4lwgjcvpoamgszkyhxgu3xhgl1l08'
          token = 'KjrEIAz6V0E8MXNFq8EKuY8PFPCcGFF1bI5vcmu8sUjihwbdsi6OAVOAqhQjulYY'
          #print(token)
          """session id 14 дней валидно, пока так оставлю потом подумаю как логиниться"""
          headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
            'cookie': f'csrftoken={token}; sessionid={session_id}'
          }
          couriers = self.parse_goodygoods(headers=headers)
          return couriers
        elif 'desertgun' in self.first_url:
          session, headers, cookies, proxies = self.log_in('login', 'password')
          couriers = self.parse_desert(session=session, headers=headers, cookies=cookies, proxies=proxies)
          return couriers


""" для тестов """  
# data = post_req_parser(parse_url='https://gonzaproject.biz/drop_request',
#  first_url='https://gonzaproject.biz/login', 
#  login='MrBugsBunny', 
#  password='BVPmhE864cg', 
#  service='Service: Gonza Project').parse()
# print((data))

# data = post_req_parser(parse_url='http://www.arsenal.st/stuffer/widgets.php?widget=drop_request',
#  first_url='http://www.arsenal.st/stuffer/login.php', 
#  login='lucianovivaldi', 
#  password='lucianovivaldi12345', 
 
#  service='arsenal [Cristal]').parse()
# print((data))

# data = post_req_parser(parse_url='http://193.37.212.30/stuffer/drops.php',
#  first_url='http://193.37.212.30/stuffer/login.php', 
#  login='MrBugsBunny', 
#  password='MrBugsBunny28', 
 
#  service='fastpack [Docent]').parse()
# print((data))

# data = post_req_parser(parse_url='http://stuffer.admwest.com/drop/index',
#  first_url='http://stuffer.admwest.com/site/login', 
#  login='luciano', 
#  password='V1valD1', 
 
#  service='Service: Leon656').parse()
# print((data))

# data = post_req_parser(parse_url='http://droid-club.com/stafer.php?action=drops',
#  first_url='http://droid-club.com/index.php', 
#  login='lucianovivaldi', 
#  password='BVPmhE864Av', 
 
#  service='Service: nalichniivp [droid club]').parse()
# print((data))

# data = post_req_parser(parse_url='http://185.43.7.183/stuffer/drops.php',
#  first_url='http://185.43.7.183/stuffer/login.php', 
#  login='lucianovivaldi', 
#  password='BVPmhE864Am', 
 
#  service='Service: USA дроп-сервис LEON [SEPTEMBER]').parse()
# print((data))

# data = post_req_parser(parse_url='https://31337.arenaproject.family/?a=page.couriers.all',
#  first_url='https://31337.arenaproject.family/?a=fnc.login&login=nordi&passw=BVPmhE864A', 
#  login='nordi', 
#  password='BVPmhE864A', 
 
#  service='Service: The arena').parse()
# print((data))

# data = post_req_parser(parse_url='https://sbx.team/?a=drop',
#  first_url='https://sbx.team/cgi-bin/index.pl', 
#  login='nordo', 
#  password='43qkonr0PN', 
 
#  service='Service: StrongBox').parse()
# print((data))

# """порешать с session_id"""
# data = post_req_parser(parse_url='https://goodygoods.services.st/courier_request/',
#  first_url='https://goodygoods.services.st/login/', 
#  login='nordioo', 
#  password='J69KRXbymj', 
 
#  service='Service: Goody Goods [Dee_Kline]').parse()
# print((data))

# data = post_req_parser(parse_url='https://desertgun.club/stuffer/drops.php',
#  first_url='https://desertgun.club/stuffer/login.php', 
#  login='lucianovivaldi', 
#  password='BVPmhE864Af', 
 
#  service='Service: amg').parse()
# print(len(data))

# data = post_req_parser(parse_url='https://tort.top/user/couriers/all',
#  first_url='https://api.tort.top/oauth/v2/token', 
#  login='Luciano', 
#  password='uD8MRvnG!V', 
#  service='Service: tortuga [Calypso]').parse()
# print((data))

# """допилить"""
# data = post_req_parser(parse_url='http://housecargo.ru/api/couriers?page=1&per=1000000&desc=true&sort=courierCreateDate&list=true',
#  first_url='http://housecargo.ru/api/login', 
#  login='lucianovivaldi', 
#  password='BVPmhE864Ar', 
 
#  service='Service: Reinhardt Drops').parse()
# print((data))

# data = post_req_parser(parse_url='https://staffer.adminpanel.digital/employees',
# first_url='https://staffer.adminpanel.digital/login', 
# login='lucianovivaldi2', 
# password='lucianovivaldi2', 

# service='Service: MoHomax').parse()
# print((data))
# http://185.43.7.183/stuffer/drops.php http://185.43.7.183/stuffer/login.php lucianovivaldi BVPmhE864Am Service: USA дроп-сервис LEON [SEPTEMBER]


