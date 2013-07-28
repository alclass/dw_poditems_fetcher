#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

test_each_process_function_script_by_script.py
Created on 28/jul/2013

@author: friend
'''
import glob, os

def chdir_to_the_scripts_folder():
  this_scripts_abspath = os.path.abspath(__file__)
  the_folders_abspath, _ = os.path.split(this_scripts_abspath)
  os.chdir(the_folders_abspath)

def process():
  chdir_to_the_scripts_folder()
  py_module_filenames = glob.glob('*.py')
  for py_module_filename in py_module_filenames:
    if py_module_filename == 'test_each_process_function_script_by_script.py':
      # this one is not to be executed !!!
      continue
    module_name, _ = os.path.splitext(py_module_filename)
    import_instruction = 'import %s' %module_name
    exec(import_instruction)
    invoke_process_function_instruction = '%s.process()' %module_name
    users_cli_msg = 'About to invoke %s :: press [ENTER] to continue. ' %invoke_process_function_instruction
    _ = raw_input(users_cli_msg)
    try:
      exec(invoke_process_function_instruction)
    except AttributeError:
      print 'There is not a process() function in %s. Continuing.' %module_name
        
if __name__ == '__main__':
  process()
