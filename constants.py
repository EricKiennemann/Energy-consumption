API_OPEN_DATA_TIMEOUT = 5
API_OPEN_DATA_RETRIES = 3
API_OPENDATA_DATASET = 'conso-elec-gaz-annuelle-par-secteur-dactivite-agregee-iris'
API_OPENDATA_SERVER = 'https://opendata.agenceore.fr/api'
DB_OLD_DATE = '1975-01-01'
PLOT_QUANTILE  =(0,0.1,0.75,0.9,0.98,0.99,0.995)
YEAR_ENERGY_API  = 2019

ENERGY_NEW_INDIVIDUAL = 23.5
ENERGY_OLD_INDIVIDUAL = 26.0
ENERGY_NEW_BUILDING = 13.0
ENERGY_OLD_BUILDING = 17.0

TOPO_DATE = '2020-12-15'
TOPO_VER = 'BDTOPO_3-0_'
TOPO_TYPE = 'TOUSTHEMES_SHP_LAMB93'

IRIS_DATE = '2020-01-01'
IRIS_VER = 'IRIS-GE_2-0_'
IRIS_TYPE = 'SHP_LAMB93'

DB_NAME = "Energy"
DB_SCHEMA = "public"
DB_HOST = "localhost"
DB_USER = 'to be moved to .env file'            #TODO
DB_PASSWORD = 'to be moved to .env file'        #TODO
DB_PORT = "5432"

FTP_TOPO_SERVER = 'ftp3.ign.fr'
FTP_TOPO_USER = 'to be moved to .env file'      #TODO
FTP_TOPO_PASSWORD = 'to be moved to .env file'  #TODO

FTP_IRIS_SERVER = 'ftp3.ign.fr'
FTP_IRIS_USER = 'to be moved to .env file'      #TODO
FTP_IRIS_PASSWORD = 'to be moved to .env file'  #TODO


INPUT_DIR = 'input'
OUTPUT_DIR = 'output'