from couriers_parser.req_pars import patterned_site_parser
from couriers_parser.pars_req_post import post_req_parser
import sys

from data.list_of_sites import list_
from couriers_parser.unick_login_cases import parse_google, parse_hr, parse_unick_cases
from database.database import db
import datetime
import re

from couriers_parser.desert import parse_d
res_ = []

def main():
  start = datetime.datetime.now()
  
  """ инициализация класса дб и создание таблицы """
  db_ = db()
  db_.create_table()

  """ 
      список 'хороших' сайтов, откуда удалось получить данные, позже он сравнивается со списком 
      list_ из файла data/list_of_sites 
  """
  good_services_container = []

  """ парсинг сайтов с однотипным стандартным логином """
  with open(r'data/sites_with_CSRF', 'r', encoding='utf8') as f:
      for i in f.readlines():
          passw = i.split()[3]
          parse_url = i.split()[0]
          first_url = i.split()[1]
          username = i.split()[2]
          is_unick = i.split()[4]
          
          service = re.findall(r'Service: [\w\W]+', i)[0][8:].strip()
          print(f'now is going parsing: {service} ({parse_url})...')
          try:
            data = patterned_site_parser(parse_url=parse_url,
                                        password=passw,
                                        login=username,
                                        first_url=first_url,
                                        is_unick=is_unick,
                                        service=service).parse()
            if len(data) > 0:
              good_services_container.append(service)
          except Exception as e:
            print(e, '\n', service)

          # print(data)
          #print(data)
          if data:
            for i in data:
                res_.append(i)
   #""" парсинг сайтов с 'уникальным' логином, используя пост запросы """
  with open(r'data/sites_req_post.txt', 'r', encoding='utf8') as f:
    for row in f.readlines():
      #print(row)
      site_data = row.split()
      data_page_url = site_data[0]
      url_login = site_data[1]
      username = site_data[2]
      passw = site_data[3]
      service = re.findall(r'Service: [\w\W]+', row)[0][8:].strip()
      
      print(f'now is going parsing: {service} ({data_page_url})...')                      
      try:
        scrapper = post_req_parser(first_url=url_login,
                                  login=username,
                                  password=passw,
                                  parse_url=data_page_url,
                                  service=service).parse()
        if len(scrapper) > 0:
          good_services_container.append(service)
        
        for i in scrapper: 
          
          res_.append(i)
      except Exception as e:
        print(e, '\n', service)

        
  """ парсинг сайта-гугл-таблиц(нужен апи ключ) """
  with open(r'data/google.txt', 'r', encoding='utf8') as f:
    for row in f.readlines():
      site_data = row.split()
      data_page_url = site_data[0]
      service = re.findall(r'Service: [\w\W]+', row)[0][8:].strip()
      print(f'now is going parsing: {service} ({data_page_url})...')
      try:
        scrapper = parse_google(url=data_page_url,
                                    service=service).main()
        if len(scrapper) > 0:
          good_services_container.append(service)
        for i in scrapper: 
          res_.append(i)
      except Exception as e:
        print(e, '\n', service)
  """сайт перенесли мб перенесут обратно"""
  with open('data/goody.txt', 'r', encoding='utf8') as f:
    for row in f.readlines():
      site_data = row.split()
      data_page_url = site_data[0]
      service = re.findall(r'Service: [\w\W]+', row)[0][8:].strip()
    
      try:

        scrapper = parse_unick_cases(login_url='https://goodygoods.services.st/login/',
                                    username='nordioo',
                                    passw='J69KRXbymj',
                                    parse_url='https://goodygoods.services.st/courier_request/',
                                    service='Goody Goods [Dee_Kline]').main()
        if len(scrapper) > 0:
          good_services_container.append(service)
        for i in scrapper: 
          res_.append(i)
      except Exception as e:
            print(e, '\n', service)
  
  """ разъеб клауда """
  try:
    amd = parse_d()
    if len(amd) > 0: good_services_container.append('AMG STUFF [Franklin]')
    [res_.append(i) for i in amd]
  except Exception as e:
    print(e)

  """ дроп таблицы и ее создание """
  db_.drop_table()
  db_.create_table()
  """ добавление курьеров в бд """
  for courier in res_[1:]:
    if not db_.is_courier_in_db(zip_index=courier['zip_code'],
                               service=courier['website']):
      
      db_.add_courier(city=courier['city'], 
                     region=courier['state'], 
                     zip_index=courier['zip_code'], 
                     status=courier['status'], 
                     expired=courier['expired'], 
                     site=courier['website'])

  """ очистка файла со статусами и запись информации об успешности парсинга """
  with open(r'data/statuses.txt', 'w', encoding='utf8') as f:
    f.write('')

  with open(r'data/statuses.txt', 'w', encoding='utf8') as f:
    for service in list_:
        
        if service in good_services_container:
          f.write(f'{service} OK\n')
        else:
          f.write(f'{service} FAILED\n')

  """время работы скрипта, для тестов"""
  end = datetime.datetime.now()
  res = end - start

if __name__=='__main__':
  main()
