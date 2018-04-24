#! python3
#  multiDownloadXKCD - multi threaded version of the XKCD comic downloader

import threading
import requests
import bs4
import os

os.makedirs('xkcd',exist_ok=True)

def downloadXKCD(startComic, endComic):
    for urlNumber in range (startComic, endComic):
        #Download the page
        print('Downloading page http://xkcd.com/%s...' % (urlNumber))
        res = requests.get('http://xkcd.com/%s' % (urlNumber))
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text)

        #Find the URL of the comic image
        comicElem = soup.select('#comic img')
        if comicElem == []:
            print('Could not find comic image')
        else:
            try:
                comicUrl = comicElem[0].get('src').strip("http://")
                comicUrl = "http://"+comicUrl
                if 'xkcd' not in comicUrl:
                    comicUrl = comicUrl[:7]+'xkcd.com/'+comicUrl[7:]
                #Download the image
                print('Downloading image %s...' % (comicUrl))
                res = requests.get(comicUrl)
                res.raise_for_status()

                #Save image to the created folder
                imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
            except requests.exceptions.MissingSchema:
                print('Skipping comic $s' % (comicUrl))
                continue
                

#Create and Start Thread objects
downloadThreads = []
#14 Threads, Each for 100 comics
for i in range(1,1401,100):
    downloadThread = threading.Thread(target=downloadXKCD,args=(i,i+99))
    downloadThreads.append(downloadThread)
    downloadThread.start()

#Wait for all threads to end
for downloadThread in downloadThreads:
    downloadThread.join()
print('Done.')
