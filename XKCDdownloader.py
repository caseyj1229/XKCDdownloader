#! python3
#  XKCDdownloader - downloads all the XKCD comics
import os
import requests
import bs4

url = 'http://xkcd.com'             #starting url
os.makedirs('xkcd',exist_ok = True)   #store comics in ./xkcd
count = 0                           #count of comics downloaded
while not url.endswith('#'):
    #TODO Download the page
    print('Downloading page %s...' % (url))
    res = requests.get(url,'lxml')
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text)

    #TODO Find the URL of the comic page
    comicElem = soup.select('#comic img')
    if comicElem == []:
        print('Could not find comic image')
    else:
        try:
            comicUrl=  'http:'+comicElem[0].get('src')
            #TODO Download the image
            print('Downloading image %s...' % (comicUrl))
            res = requests.get(comicUrl)
            res.raise_for_status()
        except requests.exceptions.MissingSchema:
            #skip this comic
            prevLink = soup.select('a[rel="prev"]')[0]
            url = 'http://xkcd.com' + prevLink.get('href')
            continue
        #TODO Save the image to the ./xkcd folder
        imageFile=  open(os.path.join('xkcd',os.path.basename(comicUrl)), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
    #TODO Get the Prev button's URL
    prevLink = soup.select('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prevLink.get('href')
    count += 1

print('Download Complete')
print('Total Comics Downloaded: '+str(count))
