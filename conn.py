import psycopg2
#https://gagareen.best/stuffer/drops.php https://gagareen.best/stuffer/login.php nordio EbLJprKB unick Service: Mario Bros [gagareen]
#http://stuffer.admwest.com/drop/index http://stuffer.admwest.com/site/login luciano V1valD1 Service: Leon656

conn = psycopg2.connect(
    host="localhost",
    database="couriers",
    user="postgres",
    password="postgres")
cursor = conn.cursor()
#cursor.execute("DROP TABLE couriers;")

cursor.execute("CREATE TABLE IF NOT EXISTS couriers(id serial, city text, region text, zip_index text, expired text, status text, site text)")
cursor.execute("INSERT INTO couriers(city, region, zip_index, expired, status, site) VALUES (%s,%s, %s,%s,%s,%s)", ('los-ang','фю', '11111', '11.22', 'read', 'tort') )
conn.commit()
cursor.execute("SELECT * FROM couriers;")
data = cursor.fetchall()
for i in data:
  print(i)
