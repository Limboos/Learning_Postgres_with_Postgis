import psycopg2
conn = psycopg2.connect(host='localhost', port='5432', dbname='Projekt', user='postgres', password='admin')
cursor = conn.cursor()
#ST_AsText(GeomFromEWKT('SRID=4326;POINT(111.1111111 1.1111111)')) st_astext
SQL = "select bud.gid, ST_X (St_centroid (bud.geom)),ST_Y (St_centroid (bud.geom)) from budynki bud \
where ST_Intersects(ST_Force2D(ST_Buffer(ST_GeomFromText('POINT(6432408 5664135)',2177),100, 'quad_segs=8')),bud.geom);" 
#plik wyjściowy
path=r'E:\Uczelnia\Magister\Semestr1\Programowanie_GIS\budynki_centroidy.txt'
txtfile=open(path, "w")
txtfile.write("Nr,  X,  Y\n")   

cursor.execute(SQL)
records=cursor.fetchall()

for record in records:
    lista=[str(record[0]),",", str(record[1]),",", str(record[1]), "\n"]
    txtfile.writelines(lista)
     
txtfile.close()
cursor.close()
conn.close()
