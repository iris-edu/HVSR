"""
  DESCRIPTION
    a collection of functions to work with files and directories

  HISTORY
    2019-06-03 IRIS DMC Product Team (Manoch): release V.2019.154
    2018-07-10 IRIS DMC Product Team (Manoch): pre-release V.2018.191
    2015-05-19 IRIS DMC Product Team (Manoch): created (V.2015.139)
"""

import os
import sys

hvsrDirectory   = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
libraryPath     = os.path.join(hvsrDirectory, 'lib')
sys.path.append(libraryPath)

import msgLib 


def mkdir(baseDir, dir):
   """ make a directory"""
   try:
      thisDir = os.path.join(baseDir, dir)
      if not os.path.exists(thisDir):
         os.makedirs(thisDir)
      return thisDir
   except:
      return msgLib.error('failed to create directory {}'.format(thisDir), None)


def baselineFileName(network, station, location, channel):
   """construct the baseline file name"""
   label   = '.'.join([network, station, location, channel, 'txt'])
   return label


def hvsrFileName(network,station,location,start,end):
   """construct the HVSR file name"""
   label   = '.'.join([network, station, location, start, end, 'HVSR','txt'])
   return label
