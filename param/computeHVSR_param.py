import os, sys
#
# IRIS HVSR
#
# DESCRIPTION
# computeHVSR.py configuration parameters
#
# HISTORY
#  2017-11-28 IRIS DMC Product Team (Manoch): public release R.2017332
#  2015-05-19 IRIS DMC Product Team (Manoch): created R.2017139
#
# NOTES
#

verbose = 1
parentDirectory  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

#
# import the libraries
#
libraryPath    = os.path.join(parentDirectory, 'lib')
sys.path.append(libraryPath)

import fileLib as fileLib

#
# URLs
#
mustangPsdUrl = "http://service.iris.edu/mustang/noise-psd/1/query?"
mustangPdfUrl = "http://service.iris.edu/mustang/noise-pdf/1/query?"

#
# Directories
#
dataDirectory     = fileLib.mkdir(parentDirectory,"data")
imageDirectory    = fileLib.mkdir(parentDirectory,os.path.join("image","hvsr"))
workDir           = fileLib.mkdir(parentDirectory,"scratch")
baselineDirectory = fileLib.mkdir(dataDirectory,"baseline")
hvsrDirectory     = fileLib.mkdir(dataDirectory,"hvsr")

#
# default station info
#
chan = 'BHZ,BHN,BHE'

#
# define x value type (period or frequency)
#
xtype      = "frequency"
hvsrband   = [0.1,15]

#
# minimum peak amplitude to be considered
#
waterlevel = 1

#
# minimum rank to be accepted
#
minrank = 2

#
# plot
#
plot       = 1
plotpsd    = 0
plotpdf    = 1
plotbad    = 0
yLabel     = "Power (dB)"
xLabel     = {"frequency":"Frequency (Hz)", "period":"Period (s)"}
xLim       = {"frequency":[0.001,20], "period":[0.1,120]}
yLim       = [-200,-50]
#yLim       = [-150,-70]
#yLim       = [-200,-100]

hvsrylim   = [0,5]
hvsrXlim   = hvsrband
hvsrYlabel = 'HVSR'


pMin       = -0.5
pMax       = 30

colorLow   = 'blue'
colorMid   = 'yellow'
colorHigh  = 'red'
imageDpi   = 150
imageSize  = [8,16]
alpha      = 0.7
lw         = 3
