import psycopg2

""" класс работы с базой данных postgresql"""
class db:
  def __init__(self):
    self.connection = psycopg2.connect(dbname='multipy_couriers_sites_pasr', user='postgres', 
                      password='123', host='localhost')
    print('connected to db')
    self.cursor = self.connection.cursor()
    #self.create_table()

  def create_table(self):
    with self.connection:
      
      self.cursor.execute('CREATE TABLE IF NOT EXISTS couriers(id serial, city text, region text, zip_index text, expired text, status text, site text)')
      print('created if not was beafart')
      self.connection.commit()

  def drop_table(self):
    with self.connection:
      
      self.cursor.execute('DROP TABLE couriers;')
      print('dropped ..')
      self.connection.commit()

  
  def is_courier_in_db(self, zip_index, service):
    with self.connection:
      self.cursor.execute("SELECT zip_index, site FROM couriers WHERE zip_index=%s AND site=%s", (zip_index, service))
      
      if self.cursor.fetchone():
        return True
      return False

  def get_couriers_count_in_db(self):
    with self.connection:
      self.cursor.execute("SELECT * FROM couriers")
      
      return len(self.cursor.fetchall())

  def add_courier(self, city, region, zip_index, expired, status, site):
    with self.connection:
      self.cursor.execute('INSERT INTO couriers(city, region, zip_index, expired, status, site) VALUES (%s,%s,%s,%s,%s,%s)', (city, region, zip_index, expired, status, site))
      self.connection.commit()

  def get_couriers(self):
    with self.connection:
      self.cursor.execute('SELECT * FROM couriers')
      couriers = self.cursor.fetchall()
      
    return couriers

print(db().get_couriers_count_in_db())