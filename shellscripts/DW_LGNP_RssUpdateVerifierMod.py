#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

DwLangsamNachrichtenPodcastDataMod.py
Created on 24/jul/2013

@author: friend
'''

import datetime
from datetime import date
import glob
import os
import sys

from PodItemUtils import get_pydate_from_acceptable_str_date_format

import __init__; __init__._insert_parent_dir_to_path_if_needed()
import local_settings as ls


class DW_LGNP_RssUpdateVerifier(object):

  DW_LANGSAM_NACHRICHTEN_PODCAST_RSS_URL = 'http://rss.dw.de/xml/DKpodcast_lgn_de'
  PODCAST_RSS_FILENAME_AFTER_WGET = 'DKpodcast_lgn_de'
  LOCAL_RSS_FILENAME_BASE = '%(from_str_date)s zu %(to_str_date)s DW Langsam gesprochene Nachrichten Podcast.rss.xhtml'

  def __init__(self):
    self.today = date.today()
    self.first_date_found = None
    self.last_date_found = None
    self.latest_rss_xml_filename = None

  def verify_local_rss_files(self):
    os.chdir(ls.PODITEM_DATA_ROOT_DIR)
    xhtmls = glob.glob('*.xhtml')
    for xhtml in xhtmls:
      prefix = xhtml[  : len('dd-mm-yyyy zu dd-mm-yyyy') ]
      pp = prefix.split(' ')
      from_str_date = pp[1]
      to_str_date = pp[2]
      from_date = get_pydate_from_acceptable_str_date_format(from_str_date)
      to_date   = get_pydate_from_acceptable_str_date_format(to_str_date)
      if self.first_date_found == None or from_date < self.first_date_found:
        self.first_date_found = from_date
      if self.last_date_found == None or to_date > self.last_date_found:
        self.last_date_found = to_date
        self.latest_rss_xml_filename = xhtml 
        
  def get_latest_rss_xml_file_abspath(self):
    return os.path.join(ls.PODITEM_DATA_ROOT_DIR, self.latest_rss_xml_filename)

  def should_it_pull_rss_feeds(self, reverify=False):
    if self.last_date_found == None or reverify:
      self.verify_local_rss_files()
      if self.last_date_found == None:
        return True
    elapsed = self.today - self.last_date_found
    if elapsed.days > 2:
      return True
    now = datetime.datetime.now()
    if elapsed.days == 1 and now.hour > 9:
      return True 
    return False

  def download_rss_feeds(self):
    if not self.should_it_pull_rss_feeds():
      print 'A download is not yet needed.'
      return
    os.chdir(ls.PODITEM_DATA_ROOT_DIR)
    comm = 'wget %s' %self.DW_LANGSAM_NACHRICHTEN_PODCAST_RSS_URL
    print comm
    '''
    ret_val = os.system(comm)
    if ret_val == 0:
      if os.path.isfile(self.PODCAST_RSS_FILENAME_AFTER_WGET):
        rss_xml_abspath = os.path.join(ls.PODITEM_DATA_ROOT_DIR, self.PODCAST_RSS_FILENAME_AFTER_WGET)
        extractor = DWLangsamNachrichtenRssExtractor(rss_xml_abspath)
        from_date = extractor.get_earliest_date_in_rss()
        to_date   = extractor.get_latest_date_in_rss()
        from_str_date = '%d-%02d-%02d' %(from_date.year,from_date.month,from_date.day) 
        to_str_date   = '%d-%02d-%02d' %(to_date.year,  to_date.month,  to_date.day)
        new_rss_filename = self.LOCAL_RSS_FILENAME_BASE %{'from_str_date':from_str_date, 'to_str_date':to_str_date}
        print 'Rename', self.PODCAST_RSS_FILENAME_AFTER_WGET, 'TO', new_rss_filename 
        os.rename(self.PODCAST_RSS_FILENAME_AFTER_WGET, new_rss_filename)
    '''
    

def test1():
  verifier = DW_LGNP_RssUpdateVerifier()
  verifier.should_it_pull_rss_feeds()
  verifier.download_rss_feeds()

def print_help_and_exit():
  print '''Usage:
  --download-transcript <date as dd.mm.yyyy or dd/mm/yyyy or yyyy-mm-dd or yyyymmdd>
  '''
  sys.exit(0)

def process():
  test1()

if __name__ == '__main__':
  process()
