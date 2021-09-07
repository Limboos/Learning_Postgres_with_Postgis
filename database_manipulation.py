# 1. Wprowadzanie do bazy z pliku

import psycopg2

conn = psycopg2.connect(host='localhost', port='5432', dbname='ADRESY', user='postgres', password='admin')
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS PKT (id_pkta varchar(20), geom geometry);")

SQL = "DO $$ BEGIN IF EXISTS (SELECT id_pkta FROM PKT WHERE id_pkta=%s) THEN RAISE NOTICE 'Punkt istnieje: '%s''; \
ELSE INSERT INTO PKT (id_pkta, geom) values (%s,ST_GeomFromText('POINT(%s %s %s)',2176)); END IF; END; $$;"

path = r'C:\Users\Student240914\Desktop\PycharmProjects\keylogger\dane.csv'
with open(path, "r") as txtfile:
	for linia in txtfile:
		# print (linia)
		pole = linia.split(" ")
		DATA = (pole[0], pole[0], pole[0], float(pole[2]), float(pole[1]), float(pole[3]))
		sql = SQL.format(DATA)
		cursor.execute(SQL, DATA)
print(conn.notices)
conn.commit()
txtfile.close()
cursor.execute("SELECT * FROM PKT;")
records = cursor.fetchall()
for record in records:
	print(record)
cursor.close()
conn.close()

# Wybiera parzyste numery punktów i zapisuej do pliku.

conn = psycopg2.connect(host='localhost', port='5432', dbname='ADRESY', user='postgres', password='admin')
cursor = conn.cursor()

cursor.execute("SELECT id_pkta, ST_X(geom), ST_Y(geom), ST_Z(geom) FROM PKT;")
records = cursor.fetchall()
parzyste = []
for record in records:
	if int(record[0]) % 2 == 0:
		parzyste.append(record)
with open("parzyste.txt", "w") as file:
	file.write("nr\ty\tx\tz\n")
	for line in parzyste:
		t = "\t".join(map(str, line))
		file.write(t + "\n")
file.close()
cursor.close()
conn.close()

# 3. Obliczenie pola powierzchni dla poligonu opartego na podanych punktach
import numpy as np


def PolyArea(x, y):
	return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


conn = psycopg2.connect(host='localhost', port='5432', dbname='ADRESY', user='postgres', password='admin')
cursor = conn.cursor()

cursor.execute("SELECT id_pkta, ST_X(geom), ST_Y(geom), ST_Z(geom) FROM PKT;")
records = cursor.fetchall()
x, y = [], []
for record in records:
	x.append(record[1])
	y.append(record[2])
pole = PolyArea(x, y)
print("Pole wynosi:", pole, "m2")
cursor.close()
conn.close()

# 4. Aktualizacja wysokości punktów z pliku
#    1 120.00
#    2 121.00
#    3 122.00
#    4 119.00


tabpkt = 'pkt'

conn = psycopg2.connect(host='localhost', port='5432', dbname='ADRESY', user='postgres', password='admin')
cursor = conn.cursor()

SQL1 = "SELECT * from " + str(tabpkt)
cursor.execute(SQL1)
ODP1 = cursor.fetchall()
#
path = r'C:\Users\Student240914\Desktop\PycharmProjects\keylogger\wysokosci.csv'
with open(path, "r") as txtfile:
	for new, old in zip(txtfile, ODP1):
		# print (linia)
		pole = new.split(" ")
		geom = old[1]
		SQL3 = "update " + str(
			tabpkt) + " set geom=ST_GeomFromText('POINTZ('||ST_X('" + geom + "'::geometry)||' '||ST_Y('" + geom + "'::geometry)||' '||" + str(
			pole[1]) + "||')',2176)\
        where " + pole[0] + "=" + str(old[0]) + ";"
		cursor.execute(SQL3)
		conn.commit()
cursor.execute("SELECT id_pkta, ST_X(geom), ST_Y(geom), ST_Z(geom) FROM PKT;")
records = cursor.fetchall()
for record in records:
	print(record)
cursor.close()
conn.close()
