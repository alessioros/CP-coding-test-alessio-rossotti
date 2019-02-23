#!/usr/bin/python
import ftplib
import os
import zipfile
import sys
import time

from utils import unzip_and_process_file


class FtpWebScraper():
    def __init__(self, scraper_conf, db_utils):
        self.ftp_url = scraper_conf['FTP_URL']
        self.ftp_path = scraper_conf['FTP_PATH']
        self.download_folder = os.path.join(os.getcwd(), scraper_conf['DOWNLOAD_FOLDER'])
        self.export_folder = os.path.join(os.getcwd(), scraper_conf['EXPORT_FOLDER'])
        self.download_interval = scraper_conf['DOWNLOAD_INTERVAL']
        self.n_file_limit = scraper_conf['FILE_NUM_LIMIT']
        self.db_utils = db_utils
        self.ftp = self.ftp_connect()

    def ftp_connect(self, retry=3):
        try:
            print('Connecting to FTP: {}..'.format(self.ftp_url))
            ftp = ftplib.FTP(self.ftp_url, timeout=100)
            ftp.login()
        except Exception as e:
            if retry > 0:
                retry -= 1
                return self.ftp_connect(retry)
            print('Error while connecting to {}, {}'.format(self.ftp_url, e))
            sys.exit(1)

        return ftp

    def download_time_series(self, remove_files=False, extract_zip=False):
        try:
            print('Downloading files from {} to local folder {}'
                    .format(self.ftp_path, self.download_folder))
            self.ftp.cwd(self.ftp_path)       
            os.chdir(self.download_folder)
        except OSError:     
            pass
        except ftplib.error_perm as e:       
            print('Error: could not find path {} on ftp server'.format(self.ftp_path))
            print(e)
            sys.exit(1)
        
        file_list = self.ftp.nlst()

        num_download = 0
        for file in file_list:
            try:
                local_file = os.path.join(self.download_folder, file.replace(self.ftp_path, ''))
                # avoid re-downloading if the file is already present
                if (local_file.endswith('.zip') and not os.path.isfile(local_file) and
                    num_download < self.n_file_limit or self.n_file_limit == 0):

                    self.ftp.retrbinary("RETR " + file, open(local_file, "w").write)
                    print('Downloaded {}'.format(local_file))
                    if extract_zip:
                        unzip_and_process_file(local_file, self.export_folder, self.db_utils, remove=remove_files)
                    num_download += 1
                    time.sleep(self.download_interval)
            except ftplib.error_perm, Exception:
                print('Error: File {} could not be downloaded '.format(file))

        print('{} files correctly downlaoded and processed'.format(num_download))
        os.chdir('../..')

        return num_download

    