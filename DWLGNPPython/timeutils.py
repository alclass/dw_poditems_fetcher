# -*- coding: utf-8 -*-
# local_settings.py

import datetime


array_3_letter_monther = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec',]
delta_31_days = datetime.timedelta(days=31)
def regenerate_date_decreasing_1_to_month(p_date):
  '''
  Do not use this function if days matter
  This function is useful for year/month considerations only
  This function decreases 1 to the month value
  The decrease in year, if necessary, will be done by the datetime subtraction itself
  '''
  p_date_regenerated  = datetime.date(year=p_date.year, month=p_date.month, day=28)
  date_1_month_decreased = p_date_regenerated - delta_31_days
  return date_1_month_decreased

def get_month_folder_name_from_pydate(pydate):
  month = pydate.month
  return '%02d-%s' %(month, array_3_letter_monther[month-1])