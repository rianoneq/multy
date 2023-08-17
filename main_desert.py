import sys

from data.list_of_sites import list_
from database.database import db
import datetime
import re

from couriers_parser.desert import parse

def main():
  start = datetime.datetime.now()
  
  db_ = db()
  db_.create_table()


  res_ = [i for i in parse()]

  # db_.drop_table()
  # db_.create_table()
  
  for courier in res_:
    if not db_.is_courier_in_db(zip_index=courier['zip_code'],
                                service=courier['website']):
      
      db_.add_courier(city=courier['city'], 
                     region=courier['state'], 
                     zip_index=courier['zip_code'], 
                     status=courier['status'], 
                     expired=courier['expired'], 
                     site=courier['website'])
    with open(r'data/statuse_desert.txt', 'w', encoding='utf8') as f:
      f.write('')

  with open(r'data/statuse_desert.txt', 'w', encoding='utf8') as f:
    if len(res_) > 0:
      f.write('AMG STUFF [Franklin] OK')
    else:
      f.write('AMG STUFF [Franklin] FAILED')

if __name__ == '__main__':
  main()