#
# DESCRIPTION
#   a collection of functions to work with files and directories
#
# HISTORY
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

#
# mkdir
#
def mkdir(baseDir,dir):
   try:
      thisDir = os.path.join(baseDir,dir)
      if not os.path.exists(thisDir):
         os.makedirs(thisDir)
      return thisDir
   except:
      return msgLib.error("failed to create directory "+thisDir,None)

#
# Baseline file name
#
def baselineFileName(network,station,location,channel):
   label   = '.'.join([network,station,location,channel,'txt'])
   return label

#
# HVSR file name
#
def hvsrFileName(network,station,location,start,end):
   label   = '.'.join([network,station,location,start,end,'HVSR','txt'])
   return label
