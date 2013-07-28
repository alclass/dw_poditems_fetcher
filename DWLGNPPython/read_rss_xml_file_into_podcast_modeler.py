#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

DwLangsamNachrichtenPodcastDataMod.py
Created on 24/jul/2013

@author: friend
'''

#import codecs, os
#import datetime
import glob, os
import sys
#import xml.etree.ElementTree as ET  #from lxml import etree

import __init__; __init__._insert_parent_dir_to_path_if_needed()
import local_settings as ls

from RssExtractorMod import RssExtractor
from RssUpdateVerifierMod import RssUpdateVerifier
from PodItemUtils import get_pydate_from_acceptable_str_date_format

def read_available_rss_xml_files():
  '''
  os.chdir(ls.PODITEM_DATA_ROOT_DIR)
  xhtmls = glob.glob('*.xhtml')
  for filename in xhtmls:
  '''
  #rss_xml_file_abspath = os.path.join(ls.PODITEM_DATA_ROOT_DIR, filename)
  rss_verifier = RssUpdateVerifier()
  rss_verifier.verify_local_rss_files()
  print 'first_date_found', rss_verifier.first_date_found
  print 'last_date_found', rss_verifier.last_date_found
  
def do_download_audio():
  str_date = sys.argv[2]
  p_pydate = get_pydate_from_acceptable_str_date_format(str_date)
  os.chdir(ls.PODITEM_DATA_ROOT_DIR)
  xhtmls = glob.glob('*.xhtml')
  for filename in xhtmls:
    rss_xml_file_abspath = os.path.join(ls.PODITEM_DATA_ROOT_DIR, filename)
    rss_obj = RssExtractor(rss_xml_file_abspath)
    item = rss_obj.find_item_on_date(p_pydate)
    if item != None:
      print item.poditem_title
      '''
      f = sys.stdout
      f.write(item.__unicode__())
      f.close()
      '''
      item.download_mp3()
      return

def process():
  if '--download' in sys.argv:
    do_download_audio()
    return
  read_available_rss_xml_files()
        
if __name__ == '__main__':
  process()
