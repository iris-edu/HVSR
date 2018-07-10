#
# DESCRIPTION
#   a collection of functions to work with files and directories
#
# HISTORY
#   2018-07-10 IRIS DMC Product Team (Manoch): prerelease R.2018191
#   2015-05-19 IRIS DMC Product Team (Manoch): created (R.2015139)
#
# NOTES
# os.path.dirname(__file__) gives the current directory
#
import os,sys

hvsrDirectory   = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
libraryPath     = os.path.join(hvsrDirectory, 'lib')
sys.path.append(libraryPath)

import msgLib 


def mkdir(baseDir,dir):
   """ make a directory"""
   try:
      thisDir = os.path.join(baseDir,dir)
      if not os.path.exists(thisDir):
         os.makedirs(thisDir)
      return thisDir
   except:
      return msgLib.error("failed to create directory "+thisDir,None)


def baselineFileName(network,station,location,channel):
   """construct the baseline file name"""
   label   = '.'.join([network,station,location,channel,'txt'])
   return label


def hvsrFileName(network,station,location,start,end):
   """construct the HVSR file name"""
   label   = '.'.join([network,station,location,start,end,'HVSR','txt'])
   return label
