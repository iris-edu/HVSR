import os, sys
#
# IRIS HVSR
#
# DESCRIPTION
# computeHVSR.py configuration parameters
#
# HISTORY
#  2018-06-18 IRIS DMC Product Team (Manoch): added removeOutliers parameter to allow HVSR computation without removing outliers and added method parameter that indicates the method to use for combining h1 and h2
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
# should we remove outliers?
#
removeOutliers = False

#
# minimum peak amplitude to be considered
#
waterlevel = 1

#
# minimum rank to be accepted
#
minrank = 2

# H is computed based on the selected method for combining h1 and h2
#     see: https://academic.oup.com/gji/article/194/2/936/597415
#     method:
#        (2) arithmetic mean, that is, H ≡ (HN + HE)/2, considered by Chavez-Garcia et al. (2007),
#        (3) geometric mean, that is, H ≡ √HN · HE, recommended by the SESAME project (2004) and also adopted by Picozzi et al. (2005),
#                                Haghshenas et al. (2008), Pileggi et al. (2011),
#        (4) vector summation, that is, H ≡ √H2 N + H2 E , used by Sauriau et al. (2007) and Puglia et al. (2011),
#        (5) quadratic mean, that is, H ≡ √(H2 N + H2 E )/2, considered by Bonnefoy-Claudet et al. (2006, 2008) and Fah¨ et al. (2001),
#        (6) maximum horizontal value, that is, H ≡ max {HN, HE}, used by Konno & Ohmachi (1998)
methodList = ['','','arithmetic mean','geometric mean','vector summation','quadratic mean','maximum horizontal value','DFA']
method = 4
dfa    = 0 # use Diffuse Field Assumption (0=no, 1=yes)
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
