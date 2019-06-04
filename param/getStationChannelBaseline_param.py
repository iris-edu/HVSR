"""
IRIS HVSR bundle

#DESCRIPTION:
  HVSR configuration parameters for getStationChannelBaseline

  HISTORY
    2019-06-03 IRIS DMC Product Team (Manoch): Release V.2019.154
    2018-07-10 IRIS DMC Product Team (Manoch): pre-release V.2018-191
    2017-11-16 IRIS DMC Product Team (Manoch): (V.2017.320)
    2017-03-12 IRIS DMC Product Team (Manoch): created (V.2017.071)
"""

import os
import sys

# The parent directory is one level up.
parentDirectory  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
libraryPath    = os.path.join(parentDirectory, 'lib')
sys.path.append(libraryPath)

import fileLib as fileLib

# Print more information during execution [0=no, 1=yes].
verbose          = 0
print('[INFO] libraryPath: {}'.format(libraryPath))


# MUSTANG service URL.
mustangUrl = 'http://service.iris.edu/mustang/noise-pdf/1/query?'

# Default directory paths.
dataDirectory     = fileLib.mkdir(parentDirectory, 'data')
imageDirectory    = fileLib.mkdir(parentDirectory, os.path.join('image', 'baseline'))
workDir           = fileLib.mkdir(parentDirectory, 'scratch')
baselineDirectory = fileLib.mkdir(dataDirectory, 'baseline')

# Default station channel codes.
chan = 'BHZ,BH1,BH2'

# X-axis  type ['period', 'frequency'].
xtype      = 'period'

# Percentiles to compute.
percenthigh = 90
percentmid  = 50
percentlow  = 5


# Plot parameters:

# Plot the values [0=no, 1=yes]
plot       = 0

# Type of plot for the percent values ['line', 'scatter']
percentPlotType = 'line'


# Axes label.
yLabel     = 'Power (dB)'
xLabel     = {'frequency':'Frequency (Hz)', 'period':'Period (s)'}

# Default x-axis limits for the two possible xtype above ['period', 'frequency'].
xLim       = {'frequency':[0.01, 9], 'period':[0.15, 200]}

# Default Y-axis limits.
yLim       = [-200,-50]

# Probability limits.
pMin       = -0.3
pMax       = 30

# Color of the percentile markers/lines.
colorLow   = 'black'
colorMid   = 'yellow'
colorHigh  = 'red'

# Plot resolution.
imageDpi   = 150

# Plot size.
imageSize  = [8.0, 6.0]

# Value plot transparency.
alpha      = 0.3

# Line width for the lines/markers. percentile values use 50% thicker lines.
lw         = 2
