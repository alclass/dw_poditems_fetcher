#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

DwLangsamNachrichtenPodcastDataMod.py
Created on 24/jul/2013

@author: friend
'''

#import codecs, os
import datetime
import os
import sys
import xml.etree.ElementTree as ET  #from lxml import etree


from PodItemMod import PodItemCannotBeInstantiated  
from PodItemMod import PodItem
from PodItemUtils import get_pydate_from_acceptable_str_date_format

import __init__; __init__._insert_parent_dir_to_path_if_needed()
import local_settings as ls

    
class DWLangsamNachrichtenXmlData(object):

  DW_LANGSAM_NACHRICHTEN_PODCAST_RSS_URL = 'http://rss.dw.de/xml/DKpodcast_lgn_de'

  def __init__(self, rss_xml_input_file_abspath):
    self.items = None
    self.set_rss_xml_input_file_abspath(rss_xml_input_file_abspath)
  
  def set_rss_xml_input_file_abspath(self, rss_xml_input_file_abspath = None):
    '''
    '''
    #infile = codecs.open(ls.get_poditems_rss_xml_abspath(), 'r', encoding='utf-8')
    #self.rss_xml_data = infile.read()
    if rss_xml_input_file_abspath == None or not os.path.isfile(rss_xml_input_file_abspath):
      # default it
      self.rss_xml_input_file_abspath = ls.get_poditems_rss_xml_abspath()
    else:
      self.rss_xml_input_file_abspath = rss_xml_input_file_abspath
    # now, go read this rss xml input file    
    self.set_rss_xml_data()

  def set_rss_xml_data(self, rss_xml_data = None):
    '''
    '''
    if rss_xml_data == None:
      self.rss_xml_data = open(self.rss_xml_input_file_abspath).read()
      return
    self.rss_xml_data = rss_xml_data
    

  def store_items(self, reread=False):
    if self.items != None and not reread:
      return
    self.items = []
    root = ET.fromstring(self.rss_xml_data)
    channel = root.getchildren()[0]
    xml_items = channel.findall('item')
    for xml_item in xml_items:
      try:
        item = PodItem(xml_item)
        self.items.append(item)
      except PodItemCannotBeInstantiated:
        continue
      
  def get_items(self):
    self.store_items()
    return self.items
  
  def find_item_on_date(self, p_pydate):
    self.store_items()
    for item in self.items:
      if p_pydate == item.poditem_date:
        return item
    return None

  def extract_and_list_mp3_urls(self):
    '''
    ??? to erase?
    '''
    #self.rss_xml_data = open(ls.get_poditems_rss_xml_abspath()).read()    
    self.store_items()
    for item in self.items:
      enclosure = item.find('enclosure')
      pubDate = item.find('pubDate')
      str_date = 'unknown'
      if pubDate != None:
        str_date = pubDate.text 
      if enclosure == None:
        continue
      url = enclosure.get('url')
      # type, length
      print url, '#', str_date
  
  
  def find_item_on_date(self, pydate):
    self.store_items()
    for item in self.items:
      if pydate == item.poditem_date:
        return item
    return None

  def list_items_simplified(self):
    '''
    '''
    self.store_items()
    for i, item in enumerate(self.items):
      print i+1, item.poditem_title

  def write_transcription_for_current_rss_xml_items(self):
    '''
    '''
    self.store_items()
    for item in self.items:
      item.write_individual_transcription_file()


def test_xml():
  poddata = DWLangsamNachrichtenXmlData()
  poddata.extract_and_list_mp3_urls() # write_transcription_for_current_rss_xml_items()

def print_help_and_exit():
  print '''Usage:
  --download-transcript <date as dd.mm.yyyy or dd/mm/yyyy or yyyy-mm-dd or yyyymmdd>
  '''
  sys.exit(0)

def download_transcript():
  try:
    german_str_date = sys.argv[2]
  except IndexError:
    print_help_and_exit()
  pydate = get_pydate_from_acceptable_str_date_format(german_str_date)
  if pydate == None or type(pydate) != datetime.date:
    print 'Date (%s) could not be understood. Please, retry.' %german_str_date
    print_help_and_exit()
  dwln_xml_data = DWLangsamNachrichtenXmlData()
  poditem = dwln_xml_data.find_item_on_date(pydate)
  print 'poditem:', poditem.poditem_title
  # poditem.download_mp3()
  poditem.write_individual_transcription_file() 
  
  
def process():
  if '--download-transcript' in sys.argv:
    download_transcript()
  # test_xml()
  # DwLangsamNachrichtenPodcast()
        
if __name__ == '__main__':
  process()
