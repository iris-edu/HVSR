"""
  DESCRIPTION
    a collection of functions to work with files and directories

  HISTORY
    2020-02-24 IRIS DMC Product Team (Manoch): style update V.2020.055
    2019-06-03 IRIS DMC Product Team (Manoch): release V.2019.154
    2018-07-10 IRIS DMC Product Team (Manoch): pre-release V.2018.191
    2015-05-19 IRIS DMC Product Team (Manoch): created (V.2015.139)
"""

import os
import sys

hvsr_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
library_path = os.path.join(hvsr_directory, 'lib')
sys.path.append(library_path)

import msgLib


def mkdir(base_directory, target_directory):
    """ Make a directory if it does not exist."""
    try:
        _directory = os.path.join(base_directory, target_directory)
        if not os.path.exists(_directory):
            os.makedirs(_directory)
        return _directory
    except Exception as _er:
        return msgLib.error(f'failed to create directory {_directory}\n{_er}', None)


def baselineFileName(network, station, location, channel):
   """Construct the baseline file name."""
   label = '.'.join([network, station, location, channel, 'txt'])
   return label


def hvsrFileName(network, station, location, start, end):
   """Construct the HVSR file name."""
   label = '.'.join([network, station, location, start, end, 'HVSR', 'txt'])
   return label
