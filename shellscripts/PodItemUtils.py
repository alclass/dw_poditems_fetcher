#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

'''

from datetime import date
import string

def get_pydate_from_str_date_having_the_separatorless_yyyymmdd_format(str_date):
  try:
    year  = int(str_date[0:4])
    month = int(str_date[4:6])
    day   = int(str_date[6:8])
    try:
      pydate = date(year=year, month=month, day=day)
      return pydate
    except ValueError:
      pass
  except ValueError:
    pass
  return None

def get_pydate_from_str_date_having_a_separatorful_yyyymmdd_format(str_date, separator='/'):
  try:
    pp    = str_date.split(separator)
    year  = int(pp[0])
    month = int(pp[1])
    day   = int(pp[2])
    try:
      pydate = date(year=year, month=month, day=day)
      return pydate
    except ValueError:
      pass
  except IndexError:
    pass
  return None

  
only_number_digits_in_str_lambda = lambda s: s in string.digits  
def only_number_digits_in_str(str_date):
  bool_list_result = map(only_number_digits_in_str_lambda, str_date)
  if False in bool_list_result:
    return False
  return True
  
def get_pydate_from_str_date_having_either_a_ddmmyyyy_or_a_mmddyyyy_format(str_date, separator='/', begins_with_month=False):
  try:
    pp    = str_date.split(separator)
    day   = int(pp[0])
    month = int(pp[1])
    if begins_with_month:
      swap  = day
      day   = month
      month = swap  
    year  = int(pp[2])
    try:
      pydate = date(year=year, month=month, day=day)
      return pydate
    except ValueError:
      pass
  except IndexError:
    pass
  return None

def get_pydate_solving_separator_from_str_date_or_None(str_date, begins_with_month=False): 
  if not len(str_date) in [8, 9, 10]:
    return None
  for separator in ['/','-','.']:
    pos = str_date.find(separator)
    if pos > -1:
      if pos == 4:
        if begins_with_month:
          raise ValueError, 'Logical Error, for when separator is after the 4th digit, date cannot begin with month'
        return get_pydate_from_str_date_having_a_separatorful_yyyymmdd_format(str_date, separator)
      return get_pydate_from_str_date_having_either_a_ddmmyyyy_or_a_mmddyyyy_format(str_date, separator, begins_with_month)
  return None

def get_pydate_from_acceptable_str_date_format(str_date, begins_with_month=False):
  '''
  Acceptable formats are:
  1) dd/mm/yyyy plus variations with a single digit for day or month, ie, d/mm/yyyy, dd/m/yyyy & d/m/yyyy 
  2) dd-mm-yyyy plus variations with a single digit for day or month, ie, d/mm/yyyy, dd/m/yyyy & d/m/yyyy
  3) dd.mm.yyyy plus variations with a single digit for day or month, ie, d/mm/yyyy, dd/m/yyyy & d/m/yyyy
  4) mm/dd/yyyy plus variations with a single digit for day or month, ie, d/mm/yyyy, dd/m/yyyy & d/m/yyyy
  5) mm-dd-yyyy plus variations with a single digit for day or month, ie, d/mm/yyyy, dd/m/yyyy & d/m/yyyy
  6) mm.dd.yyyy plus variations with a single digit for day or month, ie, d/mm/yyyy, dd/m/yyyy & d/m/yyyy
  7) yyyymmdd no variations are accepted in this case/format
  8) yyyy/mm/dd plus variations with a single digit for day or month, ie, d/mm/yyyy, dd/m/yyyy & d/m/yyyy
  9) yyyy-mm-dd plus variations with a single digit for day or month, ie, d/mm/yyyy, dd/m/yyyy & d/m/yyyy
  10) yyyy.mm.dd plus variations with a single digit for day or month, ie, d/mm/yyyy, dd/m/yyyy & d/m/yyyy
  
  Important: 
    1) Notice that neither ddmmyyyy or mmddyyyy is acceptable! That is, 
       if len(str_date) == 8, only one format (ie, yyyymmdd) is acceptable.
    2) Notice also that dates starting with year cannot invert/swap day with month,
       ie, it should always have month in the middle (ie, yyyy[sep]mm[sep]dd)
  '''
  if str_date == None:
    return None
  if type(str_date) == date:
    # well, if it's already a pydate, nothing to be done, return it!
    pydate = str_date
    return pydate
  if type(str_date) not in [str, unicode]:
    return None
  if len(str_date) == 8 and only_number_digits_in_str(str_date):
    return get_pydate_from_str_date_having_the_separatorless_yyyymmdd_format(str_date)
  # from here, a separator must exist and it's either '.', '-' or '/'
  return get_pydate_solving_separator_from_str_date_or_None(str_date, begins_with_month)
    
def get_pydate_from_german_str_date(german_str_date):
  return get_pydate_from_acceptable_str_date_format(german_str_date)
        
if __name__ == '__main__':
  pass

import unittest
class Test(unittest.TestCase):
  
  def setUp(self):
    self.expected_pydate_2013_7_5  = date(year=2013, month=7, day=5)
    self.expected_pydate_2013_7_25 = date(year=2013, month=7, day=25)
  
  def test_get_pydate_from_german_str_date(self):
    '''
    Test function get_pydate_from_german_str_date(german_str_date)
    Testing with '05.07.2013', ie, the above function should return 
      the same as date(year=2013, month=7, day=5)
    '''
    
    german_str_dates = [
      '05.07.2013','5.07.2013','05.7.2013','5.7.2013',
    ]
    for str_date in german_str_dates: 
      returned_pydate = get_pydate_from_acceptable_str_date_format(str_date)
      self.assertEqual(returned_pydate, self.expected_pydate_2013_7_5)

    german_str_dates = [
      '25.07.2013','25.7.2013',
    ]
    for str_date in german_str_dates: 
      returned_pydate = get_pydate_from_acceptable_str_date_format(str_date)
      self.assertEqual(returned_pydate, self.expected_pydate_2013_7_25)

  def test_get_pydate_from_acceptable_str_date_format(self):

    # 1) Test [d]d?[m]m?yyyy with the following combinations:
    str_dates = [ 
      '05/07/2013','5/07/2013','05/7/2013','5/7/2013',
      '05-07-2013','5-07-2013','05-7-2013','5-7-2013',
      '05.07.2013','5.07.2013','05.7.2013','5.7.2013',
    ] 
    for str_date in str_dates:
      # print 'str_date', str_date  
      returned_pydate = get_pydate_from_acceptable_str_date_format(str_date)
      self.assertEqual(returned_pydate, self.expected_pydate_2013_7_5)
    
    # 2) Test dd?[m]m?yyyy with the following combinations:
    str_dates = [ 
      '25/07/2013','25/7/2013',
      '25-07-2013','25-7-2013',
      '25.07.2013','25.7.2013',
    ] 
    for str_date in str_dates: 
      returned_pydate = get_pydate_from_acceptable_str_date_format(str_date)
      self.assertEqual(returned_pydate, self.expected_pydate_2013_7_25)
    
    # 3) Test [m]m?[d]d?yyyy with the following combinations:
    str_dates = [ 
      '07/05/2013','7/05/2013','07/5/2013','7/5/2013',
      '07-05-2013','7-05-2013','07-5-2013','7-5-2013',
      '07.05.2013','7.05.2013','07.5.2013','7.5.2013',
    ] 
    for str_date in str_dates: 
      returned_pydate = get_pydate_from_acceptable_str_date_format(str_date, begins_with_month=True)
      self.assertEqual(returned_pydate, self.expected_pydate_2013_7_5)
    
    # 4) Test [m]m?dd?yyyy with the following combinations:
    str_dates = [ 
      '07/25/2013','7/25/2013',
      '07-25-2013','7-25-2013',
      '07.25.2013','7.25.2013',
    ] 
    for str_date in str_dates: 
      returned_pydate = get_pydate_from_acceptable_str_date_format(str_date, begins_with_month=True)
      self.assertEqual(returned_pydate, self.expected_pydate_2013_7_25)
    
    # 5) Test with Format yyyymmdd 
    str_date = '20130705'
    returned_pydate = get_pydate_from_acceptable_str_date_format(str_date)
    self.assertEqual(returned_pydate, self.expected_pydate_2013_7_5)

    # 6) Test with Format yyyymmdd 
    str_date = '20130725'
    returned_pydate = get_pydate_from_acceptable_str_date_format(str_date)
    self.assertEqual(returned_pydate, self.expected_pydate_2013_7_25)
    
    # 7) Test with Format yyyy/mm/dd 
    str_dates = [ 
      '2013/07/05','2013/07/5','2013/7/05','2013/7/5',
      '2013-07-05','2013-07-5','2013-7-05','2013-7-5',
      '2013.07.05','2013.07.5','2013.7.05','2013.7.5',
    ] 
    for str_date in str_dates: 
      returned_pydate = get_pydate_from_acceptable_str_date_format(str_date)
      self.assertEqual(returned_pydate, self.expected_pydate_2013_7_5)

    # 8) Test with Format yyyy/mm/dd 
    str_dates = [ 
      '2013/07/25','2013/7/25',
      '2013-07-25','2013-7-25',
      '2013.07.25','2013.7.25',
    ] 
    for str_date in str_dates: 
      returned_pydate = get_pydate_from_acceptable_str_date_format(str_date)
      self.assertEqual(returned_pydate, self.expected_pydate_2013_7_25)


  def test_negative_cases(self):
    # 1) Test with Format yyyy.mm.dd with mm greater than 12 
    str_date = '2013.13.25'
    returned_pydate = get_pydate_from_acceptable_str_date_format(str_date)
    self.assertEqual(returned_pydate, None)
    # 2) Test with Format yyyy.mm.dd with dd greater than 31 
    str_date = '2013.12.32'
    returned_pydate = get_pydate_from_acceptable_str_date_format(str_date)
    self.assertEqual(returned_pydate, None)
    # 3) Test with Format yyyy.mm.dd with dd greater than 28 for a non-leap year 
    str_date = '2013.2.29'
    returned_pydate = get_pydate_from_acceptable_str_date_format(str_date)
    self.assertEqual(returned_pydate, None)

    '''
    # 3) Test with Format yyyy.mm.dd with dd greater than 31 
    str_date = '2013.12.32'
    self.assertRaises(ValueError, get_pydate_from_acceptable_str_date_format(str_date, begins_with_month=True))
    '''

if __name__ == '__main__':
  unittest.main()    
