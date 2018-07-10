#!/usr/bin/env python
#
#
################################################################################################
#
# NAME: getStationChannelBaseline.py - a Python script that uses MUSTANG's noise-pdf web service
#       to compute channel-specific noise-baseline for a given station. The algorithm is based on
#       McNamara et al. (2009)
#
# Copyright (C) 2018  Product Team, IRIS Data Management Center
#
#    This is a free software; you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation; either version 3 of the
#    License, or (at your option) any later version.
#
#    This script is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License (GNU-LGPL) for more details.  The
#    GNU-LGPL and further information can be found here:
#    http://www.gnu.org/
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# INPUTS:
#    Script expects a configuration parameter file under the "param" directory. 
#    the parameter file's name is the same as this scripts name with "_param" appended.
#
# USAGE:
#   getStationChannelBaseline.py net=netName sta=staName loc=locCode {chan=chanCode} start=2007-03-19 end=2008-10-28 {plot=[0,1] verbose=[0,1] percentlow=[10] percenthigh=[90] xtype=[period,frequency]}
#   getStationChannelBaseline.py net=IU sta=ANMO loc=00 chan=BHZ start=2002-11-19 end=2008-11-13 plot=1 verbose=1 percentlow=10 percenthigh=90
# 
#   the default values for the parameters between {} may be provided in the parameter file
#
# HISTORY:
#
#
#    2018-07-10 IRIS DMC Product Team (Manoch): prerelease version R.2018191
#    2017-11-16 IRIS DMC Product Team (Manoch): R.2017320
#    2017-03-12 IRIS DMC Product Team (Manoch): created (R.2017071)
#
# REFERENCES:
#
#    A Method to Establish Seismic Noise Baselines for Automated Station Assessment
#        D. E. McNamara, C. R. Hutt, L. S. Gee, H. M. Benz, R. P. Buland (2009)
#        http://srl.geoscienceworld.org/content/80/4/628
#
################################################################################################
#
# parameters to set initially
#
################################################################################################
version = "R.2018191"

#
# set paths
#
import os
scriptDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
script = os.path.basename(__file__)
paramPath = os.path.join(scriptDirectory, 'param')
libPath = os.path.join(scriptDirectory, 'lib')

import sys
sys.path.append(paramPath)
sys.path.append(libPath)

import numpy as np
import math
import urllib
import time
import importlib

#
# import the HVSR parameters and libraries
#
import fileLib as fileLib
import msgLib as msgLib

def usage():
   """usage message"""
   script = os.path.basename(__file__)
   import sys
   print("\n\nUSAGE(%s):\n"%(version))
   print(" ".join([script,"net=netName sta=staName loc=locCode chan=chanCode start=2007-03-19 end=2008-10-28 plot=[0,1] verbose=[0,1] percentlow=[10] percenthigh=[90] xtype=[period,frequency]"]))
   print("getStationChannelBaseline.py net=IU sta=ANMO loc=00 chan=BHZ start=2002-11-19 end=2008-11-13 plot=1 verbose=1 percentlow=10 percenthigh=90\n")
   print("\n\n\n")


def getArgs(argList):
   """get run arguments"""
   args = {}
   for i in range(1,len(argList)):
      key,value = argList[i].split('=')
      args[key] = value
   return args


def getParam(args,key,msgLib,value=None):
   """get a run argument for the given key"""
   if key in args.keys():
      msgLib.info(': '.join([key,args[key]]))
      return args[key]
   elif value is not None:
      return value;
   else:
      msgLib.error("missing parameter "+key,1)
      usage()
      sys.exit()


def addMonths(thisDate=None,add=1):
   """add number of months (add) to a given/current date"""
   import datetime
   if thisDate is None:
      today = datetime.date.today()
      month = today.month
      year  = today.year
   else:
      values = thisDate.split('-')
      if len(values) < 3:
         msgLib.error("bad date "+thisDate)
         usage()
         sys.exit()
      year  = int(values[0])
      month = int(values[1])
   month = month - 1 + add
   year  = year + (int(add) / 12)
   month = month % 12 + 1
   if month > 12:
      month -= 12
      year  += 1
   return "%4d-%02d-01"%(year,month)


def checkYRange(y,low,high):
   """check the PSD values to see if they are within the range"""
   import operator
   OK = True
   l = list(map(operator.sub,y,low))
   if min(l) < 0 :
      return False

   h = list(map(operator.sub,y,high))
   if max(h) > 0 :
      return False
         
   return OK

   
################################################################################################
#
# Main
#
################################################################################################

#
# set parameters
#
args = getArgs(sys.argv)
paramFileName = script.replace('.py','') + '_param'
print("\n\n\n")
msgLib.info(', '.join([script,paramFileName, version]))
msgLib.info('Param Path: '+paramPath)

try: 
   param = importlib.import_module(paramFileName)
   msgLib.info("loaded: "+paramFileName) 
except:
   msgLib.error("failed to load: "+paramFileName,1)
   sys.exit()


channelList = getParam(args,'chan',msgLib,param.chan)
network     = getParam(args,'net',msgLib)
if network is None:
   msgLib.error('network not defined!',1)
   sys.exit()
station     = getParam(args,'sta',msgLib)
if station is None:
   msgLib.error('station not defined!',1)
   sys.exit()
location    = getParam(args,'loc',msgLib)
if location == 'DASH':
   location = '--'
if location is None:
   msgLib.error('location not defined!',1)
   sys.exit()

percentLow  = getParam(args,'percentlow',msgLib,param.percentlow)
percentMid  = getParam(args,'percentmid',msgLib,param.percentmid)
percentHigh = getParam(args,'percenthigh',msgLib,param.percenthigh)
percentile  = [float(percentLow), float(percentMid), float(percentHigh)]

start      = getParam(args,'start',msgLib)
try:
   startTime  = time.strptime(start, "%Y-%m-%d")
except:
   msgLib.error('bad start',start)
   sys.exit()
   
end        = getParam(args,'end',msgLib)
try:
   endTime    = time.strptime(end, "%Y-%m-%d")
except:
   msgLib.error('bad end',end)
   sys.exit()
   
verbose    = int(getParam(args,'verbose',msgLib,param.verbose))
doPlot     = int(getParam(args,'plot',msgLib,param.plot))
xtype      = getParam(args,'xtype',msgLib,param.xtype)

#
# turn off the display requirement, if plot is not requested`
#
import matplotlib
if doPlot <= 0:
   msgLib.info("Plotting OFF")
   matplotlib.use('agg')
else:
   from obspy.imaging.cm import pqlx

channelIndex = -1
gotData      = False
channels     = channelList.strip().replace(' ','').split(',')
psdCount     = {}
for channel in channels:
   channelIndex += 1
   X       = []
   Y       = []
   P       = []
   xValues = []
   yValues = []
   pctLow  = []
   pctMid  = []
   pctHigh = []

   target  = '.'.join([network,station,location,channel,"M"])
   title   = ' '.join(['.'.join([network,station,location]),"Station-Channel Baseline",start,"-",end])
   label   = '.'.join([network,station,location,channelList.replace(',','-'),'PSDs',xtype,start,end])
   msgLib.info("requesting "+target+" from "+start+" to "+end)

   baselineFileName = os.path.join(param.baselineDirectory,fileLib.baselineFileName(network,station,location,channel))
   baselineFile     = open(baselineFileName,'w')
   baselineFile.write("#%s %s percentile %s percentile %s percentile\n"%('frequency',percentLow,percentMid,percentHigh))

   URL = param.mustangUrl+'target='+target+'&starttime='+start+'&endtime='+end+'&format=text'
   if verbose:
      msgLib.info('requesting:'+URL)
   try:
      link    = urllib.request.urlopen(URL)
   except urllib.error.HTTPError as e:
      gotData = False
      print ("\n")
      print(e.code)
      print(e.reason)
      print(e.headers)
      msgLib.error("failed on target "+target+" "+URL,1)
      continue
   
   msgLib.info("waiting for reply....")

   data     = link.read().decode()
   lines    = data.split('\n')
   lastFreq = ''
   gotData  = True
   lineCount        = 0
   nonBlankLastLine = 0
   if len(lines[-1].strip()) <= 0:
      nonBlankLastLine = 1
   for line in lines:
      lineCount += 1
      if len(line.strip()) <= 0:
         continue
      if line[0] == '#' or ',' not in line:
         continue

      (freq, power, hits) = line.split(',')
      if lastFreq == '':
         lastFreq = freq.strip()
         powerList = []
         powerList.append(float(power.strip()))
         hitsList  = []
         hitsList.append(int(hits.strip()))
      elif lastFreq == freq.strip():
         powerList.append(float(power.strip()))
         hitsList.append(int(hits.strip()))

      #
      # got all the counts for this bin, find the percentiles
      #
      if lastFreq != freq.strip() or lineCount == len(lines) - nonBlankLastLine:
         totalHits = sum(hitsList)
         #
         # get the number of contributing PSDs from the first bin of each channel
         #
         if channel not in psdCount.keys():
            psdCount[channel] = totalHits

         values = []
         yValues.append(np.array(hitsList)*100.0/totalHits)

         #
         # find the percentiles
         #
         for p in percentile:
            total     = 0
            thisLevel = p * float(totalHits) / 100.0

            #
            # power goes from low to high
            # here we define percentile as he smallest value in the list such that 
            # no more than P percent of the data is strictly less than the value 
            # and at least P percent of the data is less than or equal to that value
            #
            previousPower =  None
            for (currentHits, currentPower) in zip(hitsList,powerList):
               if previousPower is None:
                  previousPower = currentPower 
               total += int(currentHits)
               if float(total) == thisLevel:
                  values.append(currentPower)
                  break
               elif float(total) > thisLevel:
                  values.append(previousPower)
                  break
               previousPower = currentPower

         if xtype == "period":
            lastX = 1.0/float(lastFreq)
            xValues.append(lastX)
         else:
            lastX = float(lastFreq)
            xValues.append(lastX)

         #
         # write the baseline file
         #
         baselineFile.write("%s %0.2f %0.2f %0.2f\n"%(lastFreq,values[0],values[1],values[2]))

         #
         # save values for plot
         #
         for i in range(len(hitsList)):
            Y.append(float(powerList[i]))
            P.append(float(hitsList[i]) * 100.0 / float(totalHits))
            X.append(lastX)

         pctLow.append(values[0])
         pctMid.append(values[1])
         pctHigh.append(values[2])

         lastFreq = freq.strip()
         powerList = []
         powerList.append(float(power))
         hitsList  = []
         hitsList.append(int(hits))
   msgLib.info("baseline file:"+baselineFileName)
   baselineFile.close()

   if doPlot > 0 and gotData:

      msgLib.info("PLOT Station-Channel Baseline")
      if channelIndex == 0:
         import matplotlib.pyplot as plt
         from matplotlib  import cm
         from matplotlib.offsetbox import AnchoredText
         fig = plt.figure(figsize=(param.imageSize),facecolor="white")
         matplotlib.rcParams.update({'font.size': 6})
         fig.canvas.set_window_title(label)
         ax = []
         ax.append(plt.subplot(len(channels),1,channelIndex+1))
      else:
         ax.append(plt.subplot(len(channels),1,channelIndex+1, sharex=ax[0]))

      # define the colormap
      #cmap = plt.cm.jet
      # extract all colors from the .jet map
      #cmaplist = [cmap(i) for i in range(cmap.N)]
      # force the first color entry to be grey
      #cmaplist[0] = "mediumorchid"
      # create the new map
      #cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
      cmap = pqlx

      ok      = []
      plt.plot(np.array(xValues),pctHigh,lw=1,c=param.colorHigh,label=str(percentHigh)+'%')
      plt.plot(np.array(xValues),pctMid,lw=1,c=param.colorMid,label=str(percentMid)+'%')
      plt.plot(np.array(xValues),pctLow,lw=1,c=param.colorLow,label=str(percentLow)+'%')
      #plt.suptitle(title)
      ax[0].set_title(title)
      plt.ylabel(param.yLabel)
      plt.legend(loc='upper left')
      im = plt.scatter(X,Y,c=P, s=46.5, marker = '_',  linewidth=param.lw, edgecolor='face', cmap=cmap, alpha=param.alpha)
      ax[channelIndex].set_xscale('log')
      anchored_text = AnchoredText(' '.join(['.'.join([network,station,location,channel]),"{:,d}".format(psdCount[channel]),'PSDs']), loc=9)
      ax[channelIndex].add_artist(anchored_text)
      plt.xlim(param.xLim[xtype])
      plt.ylim(param.yLim)
      if (channelIndex+1 == len(channels)):
         plt.xlabel(param.xLabel[xtype])

      # create a second axes for the colorbar
      ax2 = fig.add_axes([0.92, 0.1, 0.01, 0.8])
      fig.colorbar(im, ax2, orientation='vertical')
      ax2.set_ylabel('Probability (%)', size=9, rotation=270, labelpad=7)
      plt.clim(param.pMin,param.pMax)

if doPlot > 0 and gotData:
   plotFileName = os.path.join(param.imageDirectory,fileLib.baselineFileName(network,station,location,channelList.replace(',','-')).replace(".txt","_"+xtype+".png"))
   plt.savefig(plotFileName,dpi=param.imageDpi)
   msgLib.info("Saved plot file: "+plotFileName)
   msgLib.info("Show")
   plt.show()

print("\n\n\n")
