import psycopg2


def runQuery(a):
    tabbud='budynki'
    tabgrd= 'grd_200'
    tabgrdinfo='grd_info'
    conn1 = psycopg2.connect(host='localhost', port='5432', dbname='Projekt', user='postgres', password='admin')

    row1 = a
    idg1 = row1[0]
    geom1 = row1[7]
    SQL1 = "SELECT COUNT(gid) nbud FROM " + str(
        tabbud) + " a where ST_Intersects('" + str(geom1) + "'::geometry,ST_Centroid(a.geom));"
    cursor1 = conn1.cursor()
    cursor1.execute(SQL1)
    odp1 = cursor1.fetchone()
    SQL1_1 = "INSERT INTO " + tabgrdinfo + "(ind,geom,nbud) VALUES (" + str(idg1) + ",'" + str(geom1) + "'::geometry," + str(
        odp1[0]) + ");"
    cursor1.execute(SQL1_1)
    conn1.commit()
    cursor1.close()


if __name__ == '__main__':
    import math
    import sys
    import re
    from pathlib import Path
    import numpy as np
    import time

    import pymp
    import pymp.config
    import os, tqdm, glob
    from multiprocessing import Pool
    import multiprocessing, time
    #-------------------------------------------------------
    tabbud='budynki'
    tabgrd= 'grd_200'
    tabgrdinfo='grd_info'

    #------------------polaczenie z baza
    conn = psycopg2.connect(host='localhost', port='5432', dbname='Projekt', user='postgres', password='admin')
    cursor = conn.cursor()

    #--dodanie kolumn
    SQL="ALTER TABLE "+tabgrd+" ADD COLUMN IF NOT EXISTS nbud integer;"
    cursor.execute(SQL)
    conn.commit()

    #utworzenie tabeli
    SQL="Create TABLE IF NOT EXISTS "+tabgrdinfo+" (ind bigint, geom  geometry(GeometryZM,2177), nbud integer);"
    cursor.execute(SQL)
    conn.commit()


    print("Polaczono z baza")
    print("Obliczenia...")
    #---------------------------------------

    SQL="SELECT * from "+ str(tabgrd)
    #print (SQL)
    cursor.execute(SQL)
    ODP=cursor.fetchall()
    nrow=cursor.rowcount
    print("Liczba pól: ",nrow)

    a=pymp.shared.array((nrow,))
    a=ODP
    start = time.time()

    with Pool(3) as p:
        for idx in p.imap_unordered(runQuery,a):
            continue
    end = time.time()
    print(end - start)

    print("Obliczono")
    #---------------zamkniecie polaczen

    cursor.close()
    conn.close()