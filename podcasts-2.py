# Usage:
#
# python podcasts.py
#        will only copy today's podcasts in to local directory
#
# python podcasts.py alldays
#        will copy all available podcasts in to local directory
#
# python podcasts.py 20170721
#        will copy podcasts published on July 21, 2017 to local directory
#
url = 'https://www.spreaker.com/ihr/show/2570030/episodes/feed-passthrough'

from bs4 import BeautifulSoup
from dateutil import parser
import urllib2, requests, time, sys

alldays = 0
today = time.strftime('%Y%m%d')

if len(sys.argv) > 1:
    if sys.argv[1] == 'alldays':
        alldays  = 1
    else:
        today = sys.argv[1] 

print today, "alldays", alldays
#sys.exit(0)

r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
items = soup.find_all('item')


start_time = time.time()
totIts = len(items)
bar_length = 20
errorLog = []
loop_ctr = 0
prev_filedate = 0

newitems = reversed(items)
for idx, item in enumerate(newitems):
    filedate = parser.parse(item.find('pubdate').text).strftime('%Y%m%d')
    title = item.find('title').text.replace(' ', '_')
    title = title.replace('/','_')
    #title = title.replace("'","")

    if filedate != prev_filedate:
        prev_filedate = filedate
        loop_ctr = 0

    loop_ctr += 1
    filename = filedate + str(loop_ctr).zfill(2) + "_" + title + ".mp3"

    if today == filedate  or  alldays > 0:
        print "PROCESS ", filename
        pass
    else:
        #print "SKIP    ", filename
        continue

    #continue

    mp3file = urllib2.urlopen(item.find('enclosure')['url'])
    try:
        output = open(filename,'wb')
        output.write(mp3file.read())
        output.close()
    except:
        errorLog.append(mp3file)

    percent = float(1.0*idx/totIts)
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    runtime = round(time.time()-start_time,2)
    sys.stdout.write("\rPercent: [{0}] {1}% completed in {2} seconds at a rate of {3} files/sec and {4} errors".format(hashes + spaces, int(round(percent * 100)), runtime,round(idx/runtime,2), len(errorLog)))
    sys.stdout.flush()
