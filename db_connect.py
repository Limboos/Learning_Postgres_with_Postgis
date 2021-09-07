
import psycopg2

conn = psycopg2.connect(host='localhost', port='5432', dbname='ADRESY', user='postgres', password='abc')
cursor = conn.cursor()

cursor.execute("create table BUDYNKI (id_bud varchar(20) primary key,n_kond integer,pow_uzyt decimal(10,2),n_lokal integer);")
#s1
cursor.execute("insert into budynki values ('1',3,120,1);")

#s2
cursor.execute("""
insert into budynki (id_bud,n_kond,pow_uzyt, n_lokal)
values ('%s', %s, %s, %s);
""",
(2,2,130,2))

#s3
cursor.execute("""
insert into budynki (id_bud,n_kond,pow_uzyt, n_lokal)
values ('%(id)s', %(nk)s, %(pu)s, %(nl)s)
""",
{'id':3,'pu':120,'nk':2,'nl':4})
#mozna zmienić kolejność wprowadzonych danych


#s4
cursor.execute("insert into budynki(id_bud,n_kond) values (%s, %s);", (4,3,))
cursor.execute("update budynki set pow_uzyt=%s,n_lokal=%s WHERE id_bud='%s';", (150,3,4,))

              
#s5
SQL="insert into budynki(id_bud,n_kond,pow_uzyt, n_lokal) values ('%s', %s, %s, %s);"
DATA=(5,3,121,1,)
cursor.execute(SQL,DATA)

#
cursor.execute("insert into budynki values ('6',2,135,2);")
cursor.execute("insert into budynki values ('7',2,125,1);")
cursor.execute("insert into budynki values ('8',3,155,3);")

#conn.commit()

cursor.execute("SELECT * FROM budynki;")
records = cursor.fetchall()
for record in records:
    print (record)

