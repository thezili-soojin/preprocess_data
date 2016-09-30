from selenium import webdriver
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
import urllib
import os
import sys
import time
import shutil
import signal
import hashlib
import errno
from socket import error as socket_error
import dlib
import cv2
import numpy as np
from skimage import io

reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

facePath = os.getcwd() + "/dlsanf"


def saveImage(contents, file_sn, ext):
	print "saveImage"
	try:
		img = contents
	except Exception, e:
		print e

	imgName = file_sn + ext
	print facePath + '/' + imgName
	try:
		imgfile = open(facePath + '/' + imgName, 'w')
		imgfile.write(contents)

		print "=================="
		print "=== Save Image ==="
		print "=================="
		print
	except Exception, e:
		print e

	print "===END==="
	return True

def GetImageURLList(sn):
    display = Display(visible=0, size=(1024, 768))
    display.start()
    browser = webdriver.Chrome()
    url = 'https://www.google.co.kr/search?q=' + sn + '&newwindow=1&source=lnms&tbm=isch'

    try:
        browser.get(url)

    except:
        print "socket error"
        browser.quit()
        time.sleep(1)
        browser = webdriver.Chrome()
        browser.get(url)
        print "send url again"

    for i in range(5):
        print i
        time.sleep(2)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        browser.execute_script("if (document.getElementById('smb')) document.getElementById('smb').click();")

    time.sleep(1)
    source = browser.page_source
    soup = BeautifulSoup(source)
    img_url_list = soup.select('div.rg_di.rg_el.ivg-i div.rg_meta')

    browser.quit()
    display.stop()

    return img_url_list


def isNumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def handler(signum, frame):
    print 'Signal handler called with signal', signum
    raise IOError("Couldn't open URL!")


if __name__ == "__main__":

    PATH = os.getcwd()
    c = False
    if len(sys.argv) == 1:
		chkIndex = 0
		listfile = "search"
		f = open(listfile + ".txt")
		searchsn = f.read().splitlines()

    elif len(sys.argv) == 2:
        chkIndex = 0
        listfile = sys.argv[1]
        f = open(listfile + ".txt")
        searchsn = f.read().splitlines()

    if not os.path.isdir(PATH + '/' + listfile):
        os.mkdir(PATH + '/' + listfile)

    while 1:

        sn = searchsn[chkIndex]

        print "sn : ", sn

        path = PATH + '/' + listfile + '/' + sn

        if not os.path.isdir(path):
            os.mkdir(path)
        # else :
        #	shutil.rmtree(path)
        #	os.mkdir(path)
        index_f = open(path + '/fileList.txt', 'w')
        file_url = open(path + '/fileURL.txt', 'w')

        img_url_list = GetImageURLList(sn)

        print len(img_url_list)

        if len(img_url_list) == 0:
            time.sleep(1)
            img_url_list = GetImageURLList(sn)

        time.sleep(1)

        for img_list in img_url_list:

            edit = str(img_list)
            start = edit.find('\"ou\":\"http')
            end = edit.rfind('\",\"ow\"')
            img_url = edit[start + 6:end]
            chk = img_url.rfind('type\u003dw')

            if chk > 0:
                img_url = img_url[:chk - 1]

            img_sn = img_url[img_url.rfind('/') + 1:]
            print img_url

            chk = img_url.rfind('.')
            ext = img_url[chk:]
            chk = len(img_url) - chk
            chkext = img_sn.rfind('.')

            if chkext > 4:
                ext = ".jpg"

            if chk < 6 or len(ext) < 5:
                print "start"
                file_sn = hashlib.md5(img_url).hexdigest()
                file_sn = file_sn

                if not os.path.isfile(path + '/' + file_sn):
                    try:
                        data = urllib.urlopen(img_url)
                    except:
                        print "[Can not open the image.]"
                        print "[======== Error ========]"
                    else:
                        try:
                            contents = data.read()
                        except Exception, e:
                            print e
                            time.sleep(1)
                            data = urllib.urlopen(img_url)
                            contents = data.read()

                        print "======================================================================"
                        print "img_url   : ", img_url
                        print "img_sn  : ", img_sn
                        print "file_sn : ", file_sn
                        print "======================================================================"
                        print

                        try:

                            # getFace(imgPath, facePath, fileList, index)
                            saveImage(contents, file_sn, ext)
                        # file(path + '/' + file_sn, 'wb').write(contents)
                        except(IOError):
                            print "[======== IOError]"
                            print img_url
                            time.sleep(1)
                        else:
                            index_f.write(img_sn + '\n')
                            file_url.write(img_url + '\n')
                else:
                    print "Overlap"

        print "[======== complate : ", sn, " ========]"
        print
        print

        index_f.close()
        file_url.close()
    # comp_f.write(sn+'\n')

    # comp_f.close()

