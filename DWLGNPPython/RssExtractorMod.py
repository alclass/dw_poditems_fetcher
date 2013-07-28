#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

DW_LGNP_RssExtractorMod.py
Created on 24/jul/2013

@author: friend
'''

import datetime
import glob
import os
import sys
import xml.etree.ElementTree as ET  #from lxml import etree

from PodItemMod import PodItemCannotBeInstantiated  
from PodItemMod import PodItem
from PodItemUtils import get_pydate_from_acceptable_str_date_format

import __init__; __init__._insert_parent_dir_to_path_if_needed()
import local_settings as ls


def get_latest_rss_file_abspath():
  os.chdir(ls.PODITEM_DATA_ROOT_DIR)
  xhtmls = glob.glob('*.xhtml')
  if len(xhtmls) == 0:
    return None
  xhtmls.sort()
  latest_xhtml = xhtmls[-1]
  xhtml_abspath = os.path.join(ls.PODITEM_DATA_ROOT_DIR, latest_xhtml)
  return xhtml_abspath

    
class RssExtractor(object):
  '''
  This class models a data extractor from the DW Langsam Nachrichten Podcast RSS feeds 
  '''

  def __init__(self, rss_xml_input_file_abspath=None):
    self.poditems = None
    self.latest_date = None
    self.set_rss_xml_input_file_abspath(rss_xml_input_file_abspath)
  
  def set_rss_xml_input_file_abspath(self, rss_xml_input_file_abspath = None):
    '''
    '''
    #infile = codecs.open(ls.get_poditems_rss_xml_abspath(), 'r', encoding='utf-8')
    #self.rss_xml_data = infile.read()
    if rss_xml_input_file_abspath == None or not os.path.isfile(rss_xml_input_file_abspath):
      # default it
      self.rss_xml_input_file_abspath = get_latest_rss_file_abspath()
      # self.rss_xml_input_file_abspath = ls.get_poditems_rss_xml_abspath()
    else:
      self.rss_xml_input_file_abspath = rss_xml_input_file_abspath
    # now, go read this rss xml input file    
    self.set_rss_xml_data()

  def set_rss_xml_data(self, rss_xml_data = None):
    '''
    '''
    if rss_xml_data == None:
      if self.rss_xml_input_file_abspath == None or not os.path.isfile(self.rss_xml_input_file_abspath):
        # Give up, nothing to be done, self.poditems will be, at this point, None
        return
      self.rss_xml_data = open(self.rss_xml_input_file_abspath).read()
    else:
      self.rss_xml_data = rss_xml_data
    self.store_poditems(reread=True)

  def store_poditems(self, reread=False):
    if self.poditems != None and not reread:
      # Do nothing, ie, self.poditems has already been set
      return
    self.poditems = []
    root = ET.fromstring(self.rss_xml_data)
    channel = root.getchildren()[0]
    xml_items = channel.findall('item')
    for xml_item in xml_items:
      try:
        item = PodItem(xml_item)
        self.poditems.append(item)
      except PodItemCannotBeInstantiated:
        continue
    self.set_earliest_and_latest_dates_in_rss()

  def set_earliest_and_latest_dates_in_rss(self):
    '''
    '''
    if self.poditems == None or len(self.poditems) == 0:
      self.earliest_date_in_rss = None
      self.latest_date_in_rss   = None
    self.earliest_date_in_rss = self.poditems[0].poditem_date
    self.latest_date_in_rss   = self.poditems[0].poditem_date
    if len(self.poditems) == 1:
      # Done!
      return
    for poditem in self.poditems[1:]:
      if poditem.poditem_date < self.earliest_date_in_rss:
        self.earliest_date_in_rss = poditem.poditem_date
      if poditem.poditem_date > self.latest_date_in_rss:
        self.latest_date_in_rss = poditem.poditem_date

  def get_latest_date_in_rss(self, reread=False):
    self.store_poditems(reread)
    return self.latest_date_in_rss

  def get_earliest_date_in_rss(self, reread=False):
    self.store_poditems(reread)
    return self.earliest_date_in_rss

  def get_poditems(self, reread=False):
    self.store_poditems(reread)
    return self.poditems
  
  def find_item_on_date(self, p_pydate, reread=False):
    self.store_poditems(reread)
    for item in self.poditems:
      if p_pydate == item.poditem_date:
        return item
    return None

  def list_items_simplified(self, reread=False):
    '''
    '''
    self.store_poditems(reread)
    for i, poditem in enumerate(self.poditems):
      print i+1, poditem.poditem_title

  def write_transcription_for_current_rss_xml_items(self):
    '''
    '''
    self.store_poditems()
    for poditem in self.poditems:
      poditem.write_individual_transcription_file()


def test_xml():
  rss_extractor = RssExtractor()
  print rss_extractor.rss_xml_input_file_abspath
  rss_extractor.list_items_simplified()

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
  dwln_xml_data = RssExtractor()
  poditem = dwln_xml_data.find_item_on_date(pydate)
  print 'poditem:', poditem.poditem_title
  # poditem.download_mp3()
  poditem.write_individual_transcription_file() 

def process():
  if '--download-transcript' in sys.argv:
    download_transcript()
  test_xml()
  # DwLangsamNachrichtenPodcast()

if __name__ == '__main__':
  process()
