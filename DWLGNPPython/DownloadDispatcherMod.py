#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

Created on 28/jul/2013

@author: friend
'''
import sys

from RssUpdateVerifierMod import RssUpdateVerifier

class DownloadDispatcher(object):
  
  
  def dispatch_download_after_date(self, last_item_saved_date):
    '''
    '''
    rss_dl_verifier = RssUpdateVerifier()
    self.set_rss_xml_input_file_abspath( rss_dl_verifier.get_latest_rss_xml_file_abspath() )
    self.store_poditems()
    for poditem in self.poditems:
      if poditem.poditem_date > last_item_saved_date:
        poditem.download_mp3()
        poditem.write_transcription_for_current_rss_xml_items()

  def __str__(self):
    return '''Dispatcher object.'''

def test1():
  dispatcher = DownloadDispatcher()
  print dispatcher

def print_help_and_exit():
  print '''Usage:
  --download-transcript <date as dd.mm.yyyy or dd/mm/yyyy or yyyy-mm-dd or yyyymmdd>
  '''
  sys.exit(0)

def process():
  test1()

if __name__ == '__main__':
  process()
