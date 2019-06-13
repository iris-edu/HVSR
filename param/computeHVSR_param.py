import os, sys
#
# IRIS HVSR
#
# DESCRIPTION
# computeHVSR.py configuration parameters
#
# HISTORY
#  2018-07-10 IRIS DMC Product Team (Manoch): prerelease R.2018191
#  2018-06-18 IRIS DMC Product Team (Manoch): added removeOutliers parameter to allow HVSR computation without removing outliers and added method parameter that indicates the method to use for combining h1 and h2
#  2017-11-28 IRIS DMC Product Team (Manoch): R.2017332
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

n = 1
#
# define x value type (period or frequency)
#
xtype      = "frequency"
hvsrband   = [0.1,15]

#
# should we remove outliers?
#
removeoutliers = 1

#
# minimum peak amplitude to be considered
#
waterlevel = 1

#
# minimum rank to be accepted
#
minrank = 2

# H is computed based on the selected method for combining h1 and h2
#     see: https://academic.oup.com/gji/article/194/2/936/597415 FOR METHODS 2-6
#     method:
#        (1) Diffuse Field Assumption
#        (2) arithmetic mean H = (HN + HE)/2 (the horizontal components are combined by using a simple mean)
#        (3) geometric mean H = Sqrt(HN . HE) (mean horizontal spectra is derived by taking square-root of the product of the two horizontal components)
#        (4) vector summation H = Sqrt(N^2 + E^2)
#        (5) quadratic mean H = Sqrt((N^2 + E^2)/2.0)
#        (6) maximum horizontal value H = Max(HN, HE)
methodList = ['','Diffuse Field Assumption','arithmetic mean','geometric mean','vector summation','quadratic mean','maximum horizontal value']
method = 4
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
