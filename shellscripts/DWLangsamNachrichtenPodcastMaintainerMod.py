#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

DwLangsamNachrichtenPodcastDataMod.py
Created on 24/jul/2013

@author: friend
'''

from datetime import date #, timedelta
#import codecs, os
#import xml.etree.ElementTree as ET  #from lxml import etree

#from PodItemMod import PodItemCannotBeInstantiated  
#from PodItemMod import PodItem

from DWLangsamNachrichtenXmlDataMod import DWLangsamNachrichtenXmlData  

import __init__; __init__._insert_parent_dir_to_path_if_needed()
import local_settings as ls
 
class DWLangsamNachrichtenPodcastMaintainer(object):
  
  def __init__(self):
    self.go_download_if_day_has_elapsed()

  def stablish_podcast_data(self):
    '''
    '''
    self.podcast_rss_obj = DWLangsamNachrichtenXmlData()
  
  def go_download_if_at_least_one_day_has_elapsed(self):
    last_item = self.podcast_rss_obj.get_last_saved_item() 
    items_to_download = last_item.pickup_days_yet_to_download()
    for item_to_download in items_to_download:
      item_to_download.fetch_mp3_and_save_transcript()

  def get_last_saved_item(self):
    '''
      
    '''
    text = open(ls.get_last_fetched_abspath()).read()
    pp = text.split('-')
    year  = int(pp[0])
    month = int(pp[1])
    day   = int(pp[2])
    counterdate = date(year=year, month=month, day=day)
    return counterdate

  def has_more_than_one_day_elapsed(self):
    '''
    '''
    counterdate = self.get_last_saved_item()
    delta = date.today() - counterdate
    if delta.days > 1:
      return True
    return False

  def pickup_next_items_to_download(self):
    '''
    '''
    #deltatime_elapsed_since = date.today() - self.poditem_date
    self.podcast_rss_obj.download_missing_podcasts_up_til_today()


def test1():
  pass

def process():
  test1()
        
if __name__ == '__main__':
  process()
