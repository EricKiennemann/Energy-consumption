import os

from ftplib import FTP

import py7zr
import re

import argparse
import shutil


from constants import FTP_IRIS_PASSWORD,FTP_IRIS_USER,FTP_IRIS_SERVER,FTP_TOPO_PASSWORD,FTP_TOPO_USER,FTP_TOPO_SERVER,TOPO_VER,TOPO_DATE,TOPO_TYPE,IRIS_VER,IRIS_DATE,IRIS_TYPE,INPUT_DIR,DB_HOST,DB_NAME,DB_PASSWORD,DB_PORT,DB_SCHEMA,DB_USER

from pathlib import Path

def upload_to_db(shpfile,dept):
    """
    Uploades shape files to PostgreSQL with org2ogr
    :param shpfile: Shapefile to upload to database
    :return: None
    """

    dbname = DB_NAME
    schema = DB_SCHEMA
    host = DB_HOST
    user = DB_USER
    password = DB_PASSWORD
    port = DB_PORT

    tablename = f'{os.path.splitext(os.path.basename(shpfile))[0]}_{dept}'.upper()

    command = f"""export PGCLIENTENCODING=LATIN1 && ogr2ogr -f "PostgreSQL" PG:"host={host} dbname={dbname} user={user} password={password} port={port}" "{shpfile}" -nln {schema}.{tablename} -lco geometry_name=geom -lco precision=NO -nlt promote_to_multi -s_srs epsg:2154 -t_srs epsg:4326"""

    os.system(command)


def get_ftp_file(server,user,password,directory,filename,dept,filedest):
    ftp = FTP(server,user,password)

    ftp.cwd(directory)

    path = os.path.join(INPUT_DIR,"7z",str(dept))
    if not os.path.exists(path):
        os.makedirs(path)

    local_file_name = os.path.join(path,filedest)

    dist_file_name = filename

    my_file = open(local_file_name, 'wb') # Open a local file to store the downloaded file
    ftp.retrbinary('RETR ' + dist_file_name, my_file.write,102400) # Enter the filename to download
    my_file.close()
    ftp.quit()


def unzip(filepath,filter_pattern,temp_dir):

    with py7zr.SevenZipFile(filepath, 'r') as archive:
        allfiles = archive.getnames()
        selective_files = [f  for f in allfiles if filter_pattern in f]
        print(selective_files)
        for f in selective_files:
            print(f)

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        archive.extract(path=temp_dir,targets=selective_files)

def ign_topo_directory(dept):
    return f"{TOPO_VER}{TOPO_DATE}"

def ign_topo_filename(dept):
    return f"{TOPO_VER}{TOPO_TYPE}_D{dept:03d}_{TOPO_DATE}.7z"

def ign_iris_directory(dept):
    return ""

def ign_iris_filename(dept):
    return f"{IRIS_VER}_{IRIS_TYPE}_D{dept:03d}_{IRIS_DATE}.7z.001"



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Get necessary files from ign ftp")

    parser.add_argument('-d', '--department', action='store',
                        dest='list_dept', type=int, nargs='*',
                        help="Examples: -d 75 92 93 94. "
                        "List of departments to get ign info from")

    opts = parser.parse_args()

    list_dept = opts.list_dept

    # for each required department
    for dept in list_dept:

        # connect to ftp ign for topo files and get 7z file
        directory = ign_topo_directory(dept)
        filename = ign_topo_filename(dept)
        print(directory)
        print(filename)
        get_ftp_file(FTP_TOPO_SERVER,FTP_TOPO_USER,FTP_TOPO_PASSWORD,directory,filename,dept,"topo.7z")

        # connect to ftp ign for iris files and get 7z file
        directory = ign_iris_directory(dept)
        filename = ign_iris_filename(dept)
        print(directory)
        print(filename)
        get_ftp_file(FTP_IRIS_SERVER,FTP_IRIS_USER,FTP_IRIS_PASSWORD,directory,filename,dept,"iris.7z")

        # unzip topo file
        unzip(f'input/7z/{dept}/topo.7z','BATIMENT.','output/tmp/7z')

        # unzip iris file
        unzip(f'input/7z/{dept}/iris.7z','IRIS_GE.','output/tmp/7z')

        #upload topo file into postgis db
        filepaths =  Path('./output/tmp/').rglob('BATIMENT.shp')
        list_filepath = [f for f in filepaths]
        print(list_filepath[0])
        upload_to_db(list_filepath[0],dept)


        #upload iris file into postgis db
        filepaths =  Path('./output/tmp/').rglob('IRIS_GE.SHP')
        list_filepath = [f for f in filepaths]
        print(list_filepath[0])
        upload_to_db(list_filepath[0],dept)

        #empty tmp directory
        shutil.rmtree('output/tmp/7z')


