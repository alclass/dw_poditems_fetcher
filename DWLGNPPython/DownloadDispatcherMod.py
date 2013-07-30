#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

Created on 28/jul/2013

@author: friend
'''
#import datetime
import sys

import __init__
from RssUpdateVerifierMod import RssUpdateVerifier
from RssExtractorMod import RssExtractor
from NewDownloadVerifierMod import NewDownloadVerifier

import local_settings as ls

class DownloadDispatcher(object):
  
  def __init__(self):
    '''
    '''
    self.rss_dl_verifier = RssUpdateVerifier()
    self.rss_extractor = RssExtractor()
    self.in_between_poditems_to_download = []
  
  def check_for_in_between_missing_ones(self):
    '''
    '''
    for item in self.rss_extractor.get_poditems():
      item.download_mp3_and_transcript_if_not_yet_done_so()
    
  def dispatch_download_after_date(self, last_item_saved_date):
    '''
    '''
    self.rss_extractor.set_rss_xml_input_file_abspath( self.rss_dl_verifier.get_latest_rss_xml_file_abspath() )
    self.rss_extractor.store_poditems()
    for poditem in self.rss_extractor.poditems:
      if poditem.poditem_date > last_item_saved_date:
        poditem.download_mp3()
        poditem.write_individual_transcription_file()

  def __str__(self):
    return '''Dispatcher object.'''

def dispatch_pending_downloads():
  dispatcher = DownloadDispatcher()
  verifier = NewDownloadVerifier()
  last_item_saved_date = verifier.get_last_item_saved_date()
  #timedelta1day = datetime.timedelta(1)
  #next_day = last_item_saved_date + timedelta1day
  print 'Dispatching for', last_item_saved_date 
  dispatcher.dispatch_download_after_date(last_item_saved_date)
  dispatcher.check_for_in_between_missing_ones()

def print_help_and_exit():
  print '''Usage:
  --download-transcript <date as dd.mm.yyyy or dd/mm/yyyy or yyyy-mm-dd or yyyymmdd>
  '''
  sys.exit(0)

def process():
  dispatch_pending_downloads()

if __name__ == '__main__':
  process()
