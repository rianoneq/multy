import requests
import re

from bs4 import BeautifulSoup

""" парсинг однотипных сайтов, тоже пост запросами, теперь по шаблону {пароль, логин, csrf_token} """
class patterned_site_parser:
    def __init__(self, first_url, login, password, parse_url, is_unick, service):
        self.first_url=first_url
        self.login=login
        self.password=password
        self.url=first_url
        self.parse_url=parse_url
        self.is_unick=is_unick
        self.service=service

    def parse_dwbh(self, session):
        parse_page = session.get(self.parse_url, headers=dict(referer=self.parse_url))
        soup = BeautifulSoup(parse_page.text, 'lxml')
            
        couriers = []
        rows = [x for x in soup.find_all('tr')]
        for i in rows:
            row_text = [x.text for x in i.find_all('td')]
            if len(row_text) == 0:
                continue
            couriers_data = {
                        "city": 'n/a',
                        "state": row_text[1].strip(),
                        "zip_code": row_text[2].strip(),  # int(get_numbers(zip_code)),
                        "status": row_text[3].strip(),
                        "expired": row_text[4].strip(),
                        "website": self.service
                    }
            couriers.append(couriers_data)

        return couriers
    
    def parse_mmm(self, session):
        parse_page = session.get(self.parse_url, headers=dict(referer=self.parse_url))
        soup = BeautifulSoup(parse_page.text, 'lxml')
        # print('mmm!', soup)

        couriers = []

        rows = [x for x in soup.find_all('tr')]
        for i in soup.select('table tr')[2:]:
            row_text = [x.text.strip() for x in i.find_all('td')]
            #print(row_text[0])
            couriers_data = {
                        "city": row_text[0],
                        "state": row_text[1],
                        "zip_code": row_text[2],  # int(get_numbers(zip_code)),
                        "status": row_text[3],
                        "expired": row_text[4] if row_text[4] != '' else 'n/a',
                        "website": self.service
                    }
            #couriers.append(couriers_data)

        parse_data2 = session.get('https://mmmpack.pro/stuffer/drops.php', headers=dict(referer=self.parse_url))
        soup = BeautifulSoup(parse_data2.text, 'lxml')
        t = soup.find('table', {'id': 'new-couriers-table'})
        for i in t.find_all('tr')[1:]:
            # print(i)
            row_text = [x.text.strip() for x in i.find_all('td')]
            if len(row_text) == 1:
                break
            couriers_data = {   
                        "city": row_text[3],
                        "state": row_text[4],
                        "zip_code": row_text[5],  # int(get_numbers(zip_code)),
                        "status": row_text[6],
                        "expired": row_text[7] if row_text[7] != '' else 'n/a',
                        "website": self.service
                    }
            couriers.append(couriers_data)
        return couriers
    
    def parse_packman(self, session):
        parse_page = session.get(self.parse_url, headers=dict(referer=self.parse_url))
        soup = BeautifulSoup(parse_page.text, 'lxml')
        couriers = []

        for i in soup.select('table tr')[2:]:
            row_text = [x.text.strip() for x in i.find_all('td')]

            couriers_data = {
                        "city": 'n/a',
                        "state": row_text[2],
                        "zip_code": row_text[3],  # int(get_numbers(zip_code)),
                        "status": row_text[4],
                        "expired": row_text[5] if row_text[5] != '' else 'n/a',
                        "website": self.service
                    }
            couriers.append(couriers_data)

        return couriers
    
    def parse_gagareen(self, session):
        parse_page = session.get(self.parse_url, headers=dict(referer=self.parse_url))
        soup = BeautifulSoup(parse_page.text, 'lxml')

        couriers = []

        for i in soup.select('tbody tr'):
            row_text = [x.text.strip() for x in i.find_all('td')]
            couriers_data = {
                        "city": row_text[3],
                        "state": row_text[4],
                        "zip_code": row_text[5],  # int(get_numbers(zip_code)),
                        "status": row_text[6],
                        "expired": row_text[7] if row_text[7] != '' else 'n/a',
                        "website": self.service
                    }
            couriers.append(couriers_data)

        return couriers
    
    def parse_regatta(self, session):
        parse_page = session.get(self.parse_url, headers=dict(referer=self.parse_url))
        soup = BeautifulSoup(parse_page.text, 'lxml')

        couriers = []

        for i in soup.select('tbody tr'):
            
            row_text = [x.text.strip() for x in i.find_all('td')]
            couriers_data = {
                        "city": 'n/a',
                        "state": row_text[3],
                        "zip_code": row_text[4].split('-')[0] if '-' in row_text[4] else row_text[4],  # int(get_numbers(zip_code)),
                        "status": row_text[5],
                        "expired": row_text[6] if row_text[6] != '' else 'n/a',
                        "website": self.service
                    }
            couriers.append(couriers_data)

        return couriers
   
    def parse_swatship(self, session):
        parse_page = session.get(self.parse_url, headers=dict(referer=self.parse_url))
        soup = BeautifulSoup(parse_page.text, 'lxml')

        couriers = []

        for i in soup.select('tbody tr'):
            row_text = [x.text.strip() for x in i.find_all('td')]
            couriers_data = {
                        "city": row_text[3],
                        "state": row_text[4],
                        "zip_code": row_text[5],  # int(get_numbers(zip_code)),
                        "status": row_text[6],
                        "expired": row_text[7] if row_text[7] != '' else 'n/a',
                        "website": self.service
                    }
            couriers.append(couriers_data)

        return couriers
    
    def parse_cbpanel(self, session):
        parse_page = session.get(self.parse_url, headers=dict(referer=self.parse_url))
        soup = BeautifulSoup(parse_page.text, 'lxml')

        data = []
        #print(soup)
        for i in soup.select('tbody tr'):
            row_text = [x.text.strip() for x in i.find_all('td')]
            
            main_data = row_text[3].split('\n')
            try:
                state = re.findall(r'[A-Z]{2,}', ''.join(row_text[3]))[0]
            except: continue
            city_ = main_data[1].replace(state, '').split(',')
            city = city_[0].strip()
            zip_index = main_data[-1].split(',')[0].strip()
            status = row_text[6].strip() 
            expired = row_text[8].strip() 


            data.append(
                {'city': city,
                'state': state,
                'zip_code': zip_index,
                'status': status,
                'expired': expired,
                'website': self.service}
            )
        return data
    
    def parse_sfreud(self, session):
        parse_page = session.get(self.parse_url, headers=dict(referer=self.parse_url))
        soup = BeautifulSoup(parse_page.text, 'lxml')
        table2 = soup.find('table', {'id':'new-couriers-table'})
        couriers = []
        for i in table2.find_all('tr'):
            # print(i)
            row_text = [x.text.strip() for x in i.find_all('td')]
            if len(row_text) < 3: continue
           
            couriers_data = {
                        "city": row_text[3],
                        "state": row_text[4] if row_text[4] else 'n/a', 
                        "zip_code": row_text[5],  # int(get_numbers(zip_code)),
                        "status": row_text[6],
                        "expired": row_text[7] if row_text[7] != '' else 'n/a',
                        "website": self.service
                    }
            couriers.append(couriers_data)
        
        return couriers
    
    def parse_yourcontrolboard(self, session):
        parse_page = session.get(self.parse_url, headers=dict(referer=self.parse_url))
        soup = BeautifulSoup(parse_page.text, 'lxml')
        couriers = []

        for i in soup.select('tbody tr'):
            row_text = [x.text.strip() for x in i.find_all('td')]
            couriers_data = {
                        "city": row_text[3],
                        "state": row_text[4],
                        "zip_code": row_text[5],  # int(get_numbers(zip_code)),
                        "status": row_text[6],
                        "expired": row_text[7] if row_text[7] != '' else 'n/a',
                        "website": self.service
                    }
            couriers.append(couriers_data)

        #print(couriers[1:])
        return couriers[1:]

    def parse_peresyloff(self, session):
        parse_page = session.get(self.parse_url, headers=dict(referer=self.parse_url))
        soup = BeautifulSoup(parse_page.text, 'lxml')
        #print(soup)
        couriers = []

        for i in soup.select('tbody tr'):
            try:
                row_text = [x.text.strip() for x in i.find_all('td')]

                adr = row_text[3].split('\n')
                city = adr[1].strip()
                state = adr[2].replace(',', '').strip()
                zip_code = adr[3].split(',')[0].strip() if 'United States' in adr[3].split(',')[1] else False
                #adr = adr[0].split(',')
                if not zip_code:
                    continue
                couriers_data = {
                            "city": city,
                            "state": state,
                            "zip_code": zip_code,  # int(get_numbers(zip_code)),
                            "status": row_text[5],
                            "expired": row_text[7] if row_text[7] != '' else 'n/a',
                            "website": self.service
                        }
                couriers.append(couriers_data)
            except IndexError:
                pass
        #print(couriers)
        return couriers

    def parse_gonzaproject(self, session):
        data = []

        for tr in self.rows:
            tds = tr.find_all('td')
            
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
 
  
    def log_in(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
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
        CSRF_data_page = session.get(self.first_url, headers=headers)
        soup = BeautifulSoup(CSRF_data_page.text, 'lxml')
        CSRFName = soup.find_all('input')[0]['value']
        CSRFToken = soup.find_all('input')[1]['value']

        data = {
            'CSRFName': CSRFName,
            'CSRFToken': CSRFToken,
            'login': self.login,
            'password': self.password
        }
        r = session.post(self.url, headers=headers, data=data)
        return session
    
    def parse(self):
        session = self.log_in()

        if self.is_unick=='unick':
            if 'dwbh.us' in self.first_url:
                couriers = self.parse_dwbh(session=session)
                return couriers
            elif 'mmmpack.pro' in self.first_url:
                couriers = self.parse_mmm(session=session)
                return couriers
            elif 'pacmania' in self.first_url:
                couriers = self.parse_packman(session=session)
                return couriers
            elif 'mario1' in self.first_url:
                couriers = self.parse_gagareen(session=session)
                return couriers
            elif 'regatta.cc' in self.first_url:
                couriers = self.parse_regatta(session=session)
                return couriers
            elif 'swatship.club' in self.first_url:
                couriers = self.parse_swatship(session=session)
                return couriers
            elif 'cbpanel.top' in self.first_url:
                couriers = self.parse_cbpanel(session=session)
                return couriers
            elif 'sfreud.cc' in self.first_url:
                couriers = self.parse_sfreud(session=session)
                return couriers
            elif 'yourcontrolboard' in self.first_url:
                couriers = self.parse_yourcontrolboard(session=session)
                return couriers
            elif 'peresyloff.top' in self.first_url:
                couriers = self.parse_peresyloff(session=session)
                return couriers
            elif 'gonzaproject.biz' in self.first_url:
                couriers = self.parse_gonzaproject(session=session)
                return couriers

        else:
            parse_page = session.get(self.parse_url, headers=dict(referer=self.parse_url))
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
        

""" для тестов """
# data = patterned_site_parser(parse_url='https://sfreud.cc/stuffer/drops.php',
#  first_url='https://sfreud.cc/stuffer/login.php', 
#  login='lucianovivaldi', 
#  password='BVPmhE864As', 
#  is_unick='unick', 
#  service='sfreud').parse()
# print((data))https://gonzaproject.biz/drop_request  BVPmhE864cg 
# data = patterned_site_parser(parse_url='https://sfreud.cc/stuffer/drops.php',
#  first_url='https://sfreud.cc/stuffer/login.php', 
#  login='lucianovivaldi', 
#  password='BVPmhE864As', 
#  is_unick='unick', 
#  service='Service: sfreud').parse()
# print((data))
# data = patterned_site_parser(parse_url='https://yourcontrolboard.com/stuffer/drops.php',
#  first_url='https://yourcontrolboard.com/stuffer/login.php', 
#  login='lucianovivaldi', 
#  password='YdLzUKmP8dQfe3wVmrgtYRew2fE6Uh', 
#  is_unick='unick', 
#  service='Galeries Lafayette').parse()
# print((data))
# data = patterned_site_parser(parse_url='https://mmmpack.pro/stuffer/widgets.php?widget=drop_request',
#  first_url='https://mmmpack.pro/stuffer/login.php', 
#  login='lucianovivaldi', 
#  password='Alucia@noviAvaldiW', 
#  is_unick='unick', 
#  service='Service: MMM [Mavrodi]').parse()
# print((data))

# data = patterned_site_parser(parse_url='https://peresyloff.top/stuffer/drops.php',
#  first_url='https://peresyloff.top/stuffer/login.php', 
#  login='lucianovivaldi', 
#  password='BVPmhE864Aa', 
#  is_unick='unick', 
#  service='Service: Peresyloff [Krass]').parse()
# print(data)

# data = patterned_site_parser(parse_url='https://pacmania.club/stuffer/widgets.php?widget=drop_request',
#  first_url='https://pacmania.club/stuffer/login.php', 
#  login='nordio', 
#  password='1Q2W3#4$', 
#  is_unick='unick', 
#  service='Service: Packman').parse()
# print(data)

# data = patterned_site_parser(parse_url='https://regatta.cc/stuffer/widgets.php?widget=drop_request', first_url='https://regatta.cc/stuffer/login.php', login='nordioo', password='Yb48kjS631', is_unick='unick', service='REGATTA').parse()
# data = patterned_site_parser(parse_url='https://swatship.club/stuffer/drops.php', first_url='https://swatship.club/stuffer/login.php', login='nordioo', password='oih0jkasd435665', is_unick='unick', service='SWAT').parse()
# data = patterned_site_parser(parse_url='https://cbpanel.top/stuffer/drops.php', 
#                              first_url='https://cbpanel.top/stuffer/login.php',
#                              login='lucianovivaldi',
#                              password='hV7$dA09',
#                              is_unick='unick',
#                              service='Carders brotherhood').parse()
# data = patterned_site_parser(parse_url='https://dwbh.us/stuffer/widgets.php?widget=drop_request', first_url='https://dwbh.us/stuffer/login.php', login='nordioo', password='2$40u7UJ25D$40u7U7F#F', is_unick='unick', service="Don't Worry, Be Happy [Norman Spears/Eger]").parse()
# data = patterned_site_parser(parse_url='https://gagareen.best/stuffer/drops.php', first_url='https://gagareen.best/stuffer/login.php', login='nordio', password='EbLJprKB', is_unick='unick', service="Mario Bros [gagareen]").parse()
# data = patterned_site_parser(parse_url='https://mario1.co/stuffer/drops.php', first_url='https://mario1.co/stuffer/login.php', login='nordio', password='EbLJprKB', is_unick='unick', service="Mario Bros [gagareen]").parse()
# print(data)