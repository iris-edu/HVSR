import os, sys
#
# IRIS HVSR
#
# DESCRIPTION
# HVSR configuration parameters for getStationChannelBaseline
#
# HISTORY
#    2017-11-16 IRIS DMC Product Team (Manoch): public release (R.2017320)
#    2017-03-12 IRIS DMC Product Team (Manoch): created (R.2017071)
#
# NOTES
#
verbose          = 0
parentDirectory  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

#
# import the libraries
#
libraryPath    = os.path.join(parentDirectory, 'lib')
print("[INFO] libraryPath:",libraryPath)
sys.path.append(libraryPath)

import fileLib as fileLib

#
# URLs
#
mustangUrl = "http://service.iris.edu/mustang/noise-pdf/1/query?"

#
# Directories
#
dataDirectory     = fileLib.mkdir(parentDirectory,"data")
imageDirectory    = fileLib.mkdir(parentDirectory,os.path.join("image","baseline"))
workDir           = fileLib.mkdir(parentDirectory,"scratch")
baselineDirectory = fileLib.mkdir(dataDirectory,"baseline")

#
# default station info
#
chan = 'BHZ,BH1,BH2'

#
# define x value type (period or frequency)
#
xtype      = "period"

#
# percentiles
#
percenthigh = 90
percentmid  = 50
percentlow  = 5

#
# plot
#
plot       = 0
yLabel     = "Power (dB)"
xLabel     = {"frequency":"Frequency (Hz)", "period":"Period (s)"}
#xLim       = {"frequency":[0.01,20], "period":[0.2,200]}
xLim       = {"frequency":[0.01,20], "period":[0.06,200]}
#yLim       = [-150,-70]
yLim       = [-200,-50]

pMin       = -0.3
pMax       = 30

colorLow   = 'black'
colorMid   = 'yellow'
colorHigh  = 'red'
imageDpi   = 150
imageSize  = [4.5,24.0]
alpha      = 1.0
lw         = 3
