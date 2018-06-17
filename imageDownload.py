import httplib

import logging
import os

import requests
import time


class ImageDownload:
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

        # 54000/54021/1-4
        startTime = time.time()
        URL = 'http://cdn-img.tadpoles.xyz/contents/videos_screenshots/%s/%s/180x135/%s.jpg'
        for i in (53000, 54000):
            for j in range(1, 999):
                for n in range(1, 4):
                    sindex = str(i)
                    jindex = str(i+j)
                    nindex = str(n)

                    name = sindex + jindex + nindex
                    url = URL % (sindex, jindex, nindex)
                    filepath = download_dir + name + ".jpg"
                    if os.path.exists(filepath):
                        print "file existed(%s):" % sindex + url
                        continue

                    r = self.download(url, filepath)
                    if r is not None:
                        print "downloaded(%s):" % sindex + url
                    else:
                        print "failed(%s):" % sindex + url
                        break
                    time.sleep(0.5)
        print "## Cost Time ##"
        print time.strftime(u"%H:%M:%S", time.gmtime(time.time() - startTime))


# main
ImageDownload().run("./images/")