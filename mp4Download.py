import httplib

import logging
import os
from datetime import timedelta, datetime

import requests
import time


class Mp4Download:
    def __init__(self):
        self.session = requests.Session()
        # httplib.HTTPConnection.debuglevel = 1
        # logging.basicConfig()
        # logging.getLogger().setLevel(logging.DEBUG)
        # requests_log = logging.getLogger("requests.packages.urllib3")
        # requests_log.setLevel(logging.DEBUG)
        # requests_log.propagate = True

    def get_filePath_fileName_fileExt(self, path):
        (filepath, longname) = os.path.split(path);
        (shortname, extension) = os.path.splitext(longname);
        return filepath, longname, shortname, extension

    def make_dir(self, path):
        if os.path.exists(path):
            return
        os.makedirs(path)

    def download(self, url, save_path):
        r = self.session.get(url)
        if r.status_code != 200:
            return None
        with open(save_path, "wb") as output:
            output.write(r.content)
        return url

    def run(self, download_dir):
        self.make_dir(download_dir)
        # time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 54000/54021/1-4
        startTime = time.time()
        URL = 'http://d.eeoai.com/%s/%s/%s/%s.mp4'
        ndate = datetime.now()
        for i in range(0, 5):
            sdate = (ndate - timedelta(days=float(i))).strftime(u"%Y%m%d")
            for i in range(0, 500):
                sindex = str(i)
                name = sindex

                url = URL % (sdate, sindex, sindex, sindex)
                filepath = download_dir + name + ".jpg"
                if os.path.exists(filepath):
                    print "file existed(%s):" % sindex + url
                    continue

                r = self.download(url, filepath)
                if r is not None:
                    print "downloaded(%s):" % sindex + url
                else:
                    print "failed(%s):" % sindex + url
                time.sleep(0.5)
        print "## Cost Time ##"
        print time.strftime(u"%H:%M:%S", time.gmtime(time.time() - startTime))


# main
Mp4Download().run("./mp4/")