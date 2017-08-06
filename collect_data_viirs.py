from ftplib import FTP
from collect_data import *
from conf import Nasa_pwd, Nasa_username

VIIRS_DIR = './VIIRS'


def download_VIIRS_data():
    ftp = FTP(host='nrt3.modaps.eosdis.nasa.gov')
    ftp.login(user=Nasa_username,passwd=Nasa_pwd)
    ftp.cwd('/FIRMS/viirs/Northern_and_Central_Africa/')
    monitor(ftp=ftp,dir=VIIRS_DIR)

if __name__ == '__main__':
    download_VIIRS_data()