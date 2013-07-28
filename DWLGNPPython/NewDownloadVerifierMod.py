#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

DwLangsamNachrichtenPodcastDataMod.py
Created on 24/jul/2013

@author: friend
'''

import datetime
from datetime import date #, timedelta
import os

#from DWLangsamNachrichtenRssExtractorMod import DWLangsamNachrichtenRssExtractor
from PodItemUtils import get_pydate_from_acceptable_str_date_format  

import __init__; __init__._insert_parent_dir_to_path_if_needed()
import local_settings as ls
from DownloadDispatcherMod import DownloadDispatcher

class LogicalError(ValueError):
  pass 

class ElapsedTimeCases:
  '''
  This is a static class, ie, a class with static attributes (in fact, logical CONSTANTS) 
    and one static method (ie, business_rule_for_acknowledging_a_new_download())
  '''
  LAST_DOWNLOAD_DATE_IN_THE_FUTURE               = (False, 0, 'LAST_DOWNLOAD_DATE_IN_THE_FUTURE')
  ELAPSED_NOT_YET_1_DAY                          = (False, 1, 'ELAPSED_NOT_YET_1_DAY')
  ELAPSED_1_DAY_AND_IT_IS_BEFORE_9H              = (False, 2, 'ELAPSED_1_DAY_AND_ITS_BEFORE_9H')
  ELAPSED_1_DAY_TODAY_IS_SATURDAY                = (True,  3, 'ELAPSED_1_DAY_TODAY_IS_SATURDAY')
  ELAPSED_1_DAY_TODAY_IS_NOT_SAT_AND_IS_AFTER_9H = (True,  4, 'ELAPSED_1_DAY_TODAY_IS_NOT_SAT_AND_IS_AFTER_9H')
  # Notice, Sunday will receive at least a 2-day difference (elapsed), for no media is release on Sat or Sun
  ELAPSED_2_DAYS_TODAY_IS_SUNDAY                 = (False, 5, 'ELAPSED_2_DAYS_TODAY_IS_SUNDAY')
  ELAPSED_2_DAYS_TODAY_IS_NOT_SUNDAY             = (True,  6, 'ELAPSED_2_DAYS_TODAY_IS_NOT_SUNDAY')
  ELAPSED_3_DAYS_IT_IS_MONDAY_BEFORE_9H          = (False, 7, 'ELAPSED_3_DAYS_IT_IS_MONDAY_BEFORE_9H')
  ELAPSED_3_DAYS_IT_IS_MONDAY_AFTER_9H           = (True,  8, 'ELAPSED_3_DAYS_IT_IS_MONDAY_AFTER_9H')
  ELAPSED_4_OR_MORE_DAYS                         = (True,  9, 'ELAPSED_4_OR_MORE_DAYS')

  @staticmethod
  def business_rule_for_acknowledging_a_new_download(today, last_having_date):
    '''
      The business rule for deciding if a new download should be available "on the other side"
      General rule:
      If it's Monday and after 9:00, last download should be at most the Friday one
      If it's Tuesday and after 9:00, last download should be at most the Monday one
      (...)
    '''
    if today <= last_having_date:
      return False
    days_elapsed    = today - last_having_date
    if days_elapsed.days >= 4:
      return ElapsedTimeCases.ELAPSED_4_OR_MORE_DAYS # True
    current_weekday = today.weekday()
    now             = datetime.datetime.now()
    if days_elapsed.days == 3:
      if current_weekday == 0 and now.hour < 9:
        return ElapsedTimeCases.ELAPSED_3_DAYS_IT_IS_MONDAY_BEFORE_9H # False
      return ElapsedTimeCases.ELAPSED_3_DAYS_IT_IS_MONDAY_AFTER_9H # True
    if days_elapsed.days == 2:
      if current_weekday == 6:
        return ElapsedTimeCases.ELAPSED_2_DAYS_TODAY_IS_SUNDAY # False
      return ElapsedTimeCases.ELAPSED_2_DAYS_TODAY_IS_NOT_SUNDAY # True
    if days_elapsed.days == 1:
      if current_weekday == 5:
        return ElapsedTimeCases.ELAPSED_1_DAY_TODAY_IS_SATURDAY # False
      if now.hour > 9:
        return ElapsedTimeCases.ELAPSED_1_DAY_TODAY_IS_NOT_SAT_AND_IS_AFTER_9H # True
      return ElapsedTimeCases.ELAPSED_1_DAY_AND_ITS_BEFORE_9H  # False
    raise LogicalError, 'All options above should have taken an IF path in the code. Some logical error appears to be present.'


class NewDownloadVerifier(object):
  
  def __init__(self):
    self.today = date.today()
    self.last_date_found = None

  def explain_situation_for_a_new_download(self):
    '''
    The 3rd element of self.new_download_case_tuple is explanatory
    Invoking method self.has_time_elapse_for_new_downloads()
    Attribute self.new_download_case_tuple becomes available, so it's printed out
    '''
    _ = self.has_time_elapse_for_new_downloads()
    print self.new_download_case_tuple

  def has_time_elapse_for_new_downloads(self):
    '''
      _if_either_1_day__or_weekend_passed
    '''
    self.last_items_date = self.get_last_item_saved_date()
    self.new_download_case_tuple = ElapsedTimeCases.business_rule_for_acknowledging_a_new_download(self.today, self.last_items_date)
    # The self.new_download_case_tuple is composed of 3 data, ie, a boolean, an int, and an explanation string
    return self.new_download_case_tuple[0] 

  def go_download_missing_ones(self):       
    rss_xml_obj = DownloadDispatcher()
    rss_xml_obj.dispatch_download_after_date(self.get_last_item_saved_date())

  def decide_if_necessary_to_go_for_download(self):
    if self.has_time_elapse_for_new_downloads():
      print 'Some download is needed. Last item is dated %s' %self.get_last_item_saved_date()
      self.go_download_missing_ones()
    print 'No download is needed.'

  def get_last_year_in_stock(self):
    '''
      This method should only be called by get_last_item_saved()
        or by a method that positions to the last year's folder 
    '''
    years_on_year_folder = []
    os.chdir(ls.PODITEM_DATA_ROOT_DIR)
    for content in os.listdir('.'):
      if os.path.isdir(content):
        try:
          year = int(content)
          if year > self.today.year:
            continue
          years_on_year_folder.append(year)
        except ValueError:
          continue
    if len(years_on_year_folder) > 0:
      year_dir = str(max(years_on_year_folder))
    else:
      year_dir = '%d' %self.today.year
      os.mkdir(year_dir)
    os.chdir(year_dir)

  def get_last_month_in_stock(self):
    '''
      This method should only be called by get_last_item_saved()
        or by a method that positions to the last year's folder 
    '''
    month_dir = None
    for month in xrange(12,0,-1):
      folder_name = '%02d-%s' %(month, ls.array_3_letter_monther[month-1])
      if os.path.isdir(folder_name):
        month_dir = folder_name
        break
    if month_dir == None:
      month_dir = '01-Jan'
      print 'Creating folder', month_dir 
      os.mkdir(month_dir)
    os.chdir(month_dir)

  def get_last_item_saved_date(self, reread=False):
    if self.last_date_found != None and not reread:
      return self.last_date_found
    self.get_last_year_in_stock()
    self.get_last_month_in_stock()
    files = os.listdir('.')
    print os.path.abspath('.')
    self.last_date_found = None
    for entry in files:
      if not os.path.isfile(entry):
        continue
      extlessname, ext = os.path.splitext(entry)
      if ext != '.mp3':
        continue
      print 'entry', entry
      try:
        str_date = extlessname.split(' ')[0]
        date_found = get_pydate_from_acceptable_str_date_format(str_date)
        if date_found != None:
          if self.last_date_found == None or date_found > self.last_date_found:
            self.last_date_found = date_found
      except IndexError:
        continue
    return self.last_date_found 
  

def test1():
  verifier = NewDownloadVerifier()
  verifier.explain_situation_for_a_new_download()

def process():
  test1()
        
if __name__ == '__main__':
  process()
