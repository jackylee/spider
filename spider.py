#!/usr/bin/env python
# BeautifulSoup version findAll not changed to find_all
import argparse
import sys
import Queue
import urllib2
import requests
import re
from BeautifulSoup import BeautifulSoup
from urlparse import urljoin
import logging


def cmdparse(args):
    parser = argparse.ArgumentParser(prog = 'spider')
    parser.add_argument('-u', help='website for spidering http://xxx.xx.xx.')
    parser.add_argument('-d', help='website depth for spidering')
    parser.add_argument('-f', help='specify logfile')
    parser.add_argument('-l', help='specify logging level')
    parser.add_argument('-thread', help='specify thread count to spidering')
    parser.add_argument('--key', help='specify keyword to match', action='store_true')
    parser.add_argument('--dbfile', help='store fetched html file to sqlite', action='store_true')
    parser.add_argument('--testself', help='test for yourself', action='store_true')
    args = vars(parser.parse_args(sys.argv[1:]))
    print args
    return args

def loginit():
    FORMAT='%(asctime)-15s %(url)s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('spider')
    return logger

def spider(host, depth, keyword):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    pat = re.compile('.*mailto.*@.*|\.(jpg|jpeg|gif|tiff|bmp)$|^$|javascript:|#.*$', re.UNICODE)
    urls = Queue.Queue()
    visited = set()
    vars = (host, 0)
    urls.put(vars)
    logger = loginit()
    while not urls.empty():
        t = urls.get()
        print t[0], t[1]
        if (t[0] not in visited) and (t[1] < depth) :
            visited.add(t[0])
            try:
                req = requests.request('GET', t[0])
            except:
                print t[0], "fetched failed"
            if req.status_code == 200:
                soup = BeautifulSoup(req.content)
                for link in soup.findAll('a', href=True):
                    ans = pat.search(unicode(link.get('href')))
                    if ans is None:
                        abslink = urljoin(t[0], link.get('href'))
                        if abslink not in visited:
                            urls.put((abslink, t[1] + 1))
                print t[0] ,"fetched"
            else:
                print t[0] ,"not fetched"
def main():
    args = cmdparse(sys.argv[1:])
    spider(args['u'], args['d'], args['key'])

if __name__ == "__main__":
    main()
