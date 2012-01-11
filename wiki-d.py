#!/1/data/ENV/bin/python


"""
todo:
fix max dir size to ~300 GB
"""

import logging,logging.config
import datetime
import os
import urllib2
import re
from subprocess import call

from BeautifulSoup import BeautifulSoup, SoupStrainer
from lxml import etree


logging.config.fileConfig('logging.conf')
flogger = logging.getLogger('console')

def mkdir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    os.chdir(dirname)

def makeMeta(identifier):
    identifier = str(identifier.strip('/'))
    f = open("%s_files.xml" % identifier, 'wb')
    f.write('<files/>')
    f.close()
    grabDate = str(datetime.date.today())
    creationDate = identifier.split('-')[-1]
    meta = { 'collection': 'wikipediadumps', 'mediatype': 'web',
             'creator': 'Wikipedia', 'date': creationDate, 'title': identifier,
             'licenseurl': 'http://creativecommons.org/licenses/by-nc-sa/3.0/us/',
             'description': 'Retrieved from wikipedia.org on %s' % grabDate }
    root = etree.Element('metadata')
    for k,v in meta.iteritems():
        subElement = etree.SubElement(root,k)
        subElement.text = v
    metaXml = etree.tostring(root, pretty_print=True,
                             xml_declaration=True, encoding="utf-8")
    ff = open("%s_meta.xml" % identifier, 'wb')
    ff.write(metaXml)
    ff.close()

def main():
    
    ''' <Perpetual Loop Auto-submit business> '''
    list_home = os.getcwd()
    readyListFileName = "ready_list.txt"
    lockFileName = readyListFileName + ".lck"
    ### Exit if last list still pending, wait for it to be renamed/removed.
    if os.access( readyListFileName, os.F_OK ) is True:
        print ( 'ABORT: %s exists (Not picked up yet? Should be renamed'
                'when retrieved by auto_submit loop!)' % readyListFileName )
        if os.access( lockFileName, os.F_OK ) is True:
            os.remove(lockFileName)
        exit(0)
    ### If lock file exists, another process is already generating the list
    if os.access( lockFileName, os.F_OK ) is True:
        print ( 'ABORT: %s lockfile exists (Another process generating list'
                'already? Should be deleted when complete!)' % lockFileName )
        exit(0)
    ### Touch a lock and list file.
    touchLi = open(readyListFileName,'wb')
    touchLi.write('')
    touchLi.close()
    touchLo = open(lockFileName, 'wb')
    touchLo.write('')
    touchLo.close()
    ''' <Peprpetual Loop Auto-submit business /> '''

    mkdir('/1/incoming/tmp/wiki-dumps')
    home = os.getcwd()
    # Get links for every Wiki Directory 
    # (i.e. aawiki/,aawikibooks/,aawiktionary/,etc.).
    url = 'http://wikipedia.c3sl.ufpr.br/'
    indexHTML = urllib2.urlopen(url).read()
    wikiList = BeautifulSoup(indexHTML, parseOnlyThese=SoupStrainer(
                             'a', href=re.compile('wik')))

    for link in wikiList:
        flogger.info('Downloading: %s' % link['href'])
        # Get links for the most recent dump in every Wiki Directory.
        # (i.e. 20110901/,20110908/,20111010/,etc.)
        itemHTML = urllib2.urlopen(url + link['href']).read()
        dirStrainer = SoupStrainer('a', href=re.compile('20'))
	print dirStrainer
        dirLinks = ( [tag for tag in BeautifulSoup(itemHTML,
                     parseOnlyThese=dirStrainer)][-1] )

        for itemDIR in dirLinks:
            identifier = ( "%s-%s" % (link['href'].strip('/'),itemDIR) )
            mkdir(identifier)
            makeMeta(identifier)
            # Get links for every file in dump directory
            # (i.e. pages-logging.xml.gz,pages-articles.xml.bz2,etc.)
            dirHTML = urllib2.urlopen(url + link['href'] + itemDIR).read()
            dirLinks = BeautifulSoup(dirHTML, parseOnlyThese=SoupStrainer(
                                    'a', href=re.compile(link['href'])))
            for dumpFile in dirLinks:
                dirURL = url + dumpFile['href'].strip('/')
                fname = dumpFile['href'].split('/')[-1]
                flogger.info('Downloading: %s' % dirURL)
                wget = 'wget -c %s' % dirURL
                execute = call(wget, shell=True)
        os.chdir(home)

    os.chdir(list_home)
    dataList = os.listdir(home)
    f = open(readyListFileName,'wb')
    f.write('\n'.join(dataList))
    f.close()
    ### Remove lock file...
    os.remove(lockFileName)

    flogger.info('YOU HAVE SO MUCH WIKI!')

if __name__ == "__main__":
    main()
