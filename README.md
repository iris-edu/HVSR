 Incorporated Research Institutions for Seismology (IRIS)
 Data Management Center (DMC)
 Data Products Team
 Horizontal to Vertical Spectral Ratio (HVSR) Toolbox

 2023-12-19
 V.2020.055


 DESCRIPTION:

The Horizontal to Vertical Spectral Ratio (HVSR) is a popular method that easily provides the predominant frequency at 
a given site. In this paper, we introduce the Incorporated Research Institutions for Seismology (IRIS) Data Management 
Center’s (DMC’s) HVSR station toolbox that is available to the community. This toolbox offers sundry ways to compute the 
ratio by providing different averaging routines. They go from the simple average of spectral ratios to the ratio of
 spectral averages. Computations take advantage of the available power spectral density and probability density function 
 estimates of the ambient noise for the seismic stations and as such, can readily be used to estimate the predominant 
 frequency of the many three-component seismic stations available from IRIS. To facilitate identification of the clear 
 HVSR peaks and estimate of the predominant frequency of station sites, this toolbox further processes the results of 
 HVSR analysis to detect and rank HVSR peaks.

This toolbox contains two tools (scripts) to assist with HVSR analysis: 1) the station baseline and 2) the HVSR tool.

   - computeStationChannelBaseline.py uses IRIS DMC’s MUSTANG noise-pdf web service to compute channel-specific 
     noise-baseline for a given station following the technique outlined by McNamara et al., 2009. The objective of this 
     script is to provide an insight into station’s ambient seismic field power characteristics. For each channel, the 
     computed baseline represents the probability density function (PDF) characteristics of the PSDs in the form of 
     median, lower and higher percentiles of the available PSDs. 
     
   - computeHVSR.py - uses IRIS DMC’s MUSTANG noise-psd and noise-pdf web services to compute HVSR for a given station 
     based on the MUSTANG hourly PSDs. HVSR estimates are obtained by converting hourly PSDs to median daily spectral 
     powers and then HVSRs are computed using one of the 6 different available methods including the Diffuse Field 
     Assumption method (DFA), as described by Sánchez-Sesma et al. (2011) or the average of spectral ratios, similar 
     to the method used by McNamara et al. (2015). Options available include:
        - Remove PSDs that fall outside the station noise baseline as computed by computeStationChannelBaseline.py 
          above (parameter: removeoutliers=0|1).
        - Compute HVSR using one of the methods below (parameter: method=1|2|3|4|5|6).
        - Output a peak rank report with ranking based on SESAME 2004 (not avaiable for DFA method)
        - The HVSR computational methods supported:
             (1) DFA, Diffuse Field Assumption method (Sánchez-Sesma et al., 2011)
                 NOTE: The MUSTANG noise-psd web service Power Spectral Density estimate for seismic channels are 
                       computed using the algorithm outlined here: 
                       (http://service.iris.edu/mustang/noise-psd/docs/1/help/)
                       This algorithm involves averaging and normalization that may result in smoothing of some of the 
                       peaks that may otherwise be observed by direct computation of FFT and DFA. With this smoothing, 
                       the DFA results tend to be closer to the vector summation method, method (4) below.

             or HVSR computation by combining the two horizontal components using one of the methods referenced by 
             Albarello and Lunedei (2013):
             (2) arithmetic mean, H ≡ (HN + HE)/2
             (3) geometric mean, H ≡ √HN · HE
             (4) vector summation, H ≡ √H2 N + H2 E 
             (5) quadratic mean, H ≡ √(H2 N + H2 E )/2
             (6) maximum horizontal value, H ≡ max {HN, HE}

    CHANGES.txt
       - a text file containing the history of changes to this bundle

    INSTALL.txt
       - installation notes

    README.md
       - this file

    bin/
       - scripts directory containing:
            + computeStationChannelBaseline.py (described above)
            + computeHVSR.py (described above)
   
    param/
       - parameters directory containing:
            + getStationChannelBaseline_param.py - the configuration parameter file for the computeStationChannelBaseline.py script above
            + computeHVSR_param.py - the configuration parameter file for the computeHVSR.py script above

    lib/
       - bundle library files:
            + fileLib.py - a collection of functions to work with files and directories
            + msgLib.py - a collection of functions to print messages

 INSTALLATION:

    see the INSTALL.txt file


USAGE:
   
getStationChannelBaseline.py net=netName sta=staName loc=locCode chan=chanCode
	start=2007-03-19 end=2008-10-28 plot=[0|1] plotnnm=[0|1]verbose=[0, 1] percentlow=[10] 
	percenthigh=[90] xtype=[period,frequency]

net		station network code
sta		station code
loc		station location code
chan		station channel code (separate multiple channel codes by comma); 
		default: BHZ,BH1,BH2
xtype		X-axis  type; default: period
start		start date of the interval for which station baseline is computed (format YYYY-MM-DD).
		The start day begins at 00:00:00 UTC
end		end date of the interval for which station baseline is computed (format YYYY-MM-DD).
		The end day ends at 23:59:59 UTC

		NOTE: PSD segments will be limited to those starting between start (inclusive) and 
		end (exclusive) except when start and end are the same (in that case, the range will 
		cover start day only).

verbose		Run in verbose mode to provide informative messages [0=no, 1=yes];
		default:0
percentlow	lowest percentile to compute (float); default 5
percenthigh	Highest percentile to compute (float); default 90
plot		plot values [0|1]
plotnnm		plot the New Noise Models [0|1], active if plot=1


computeHVSR.py net=netName sta=staName loc=locCode chan=chanCodes start=2013-01-01 end=2013-01-01
plot=[0, 1] plotbad=[0|1] plotpsd=[0|1] plotpdf=[0|1] plotnnm=[0|1] verbose=[0|1] ymax=[maximum Y value]
xtype=[frequency|period] n=[number of segments] removeoutliers=[0|1] method=[1-6] showplot=[0|1]

net		station network code
sta		station code
loc		station location code
chan	station channel code (separate multiple channel codes by comma); 
		default: BHZ,BHN,BHE
xtype	X-axis  type; default: frequency
start	start date of the interval for which HVSR to be computed (format YYYY-MM-DD).
		The start day begins at 00:00:00 UTC
end		end date of the interval for which station baseline is computed (format YYYY-MM-DD).
		The end day ends at 23:59:59 UTC

		NOTE: PSD segments will be limited to those starting between start (inclusive) and 
		end (exclusive) except when start and end are the same (in that case, the range will 
		cover start day only).

verbose		Run in verbose mode to provide informative messages [0=no, 1=yes];
		    default:1
plotbad		plot rejected PSDs (float) if "plotpsd" option is selected; default 0
plotnnm		plot the New Noise Models [0|1], active if plot=1; default 1
plotpsd		plot PSDs; default 0
plotpdf		plot PSD\DFs; default 1
ymax		maximum Y values; default -50
n		    break start-end interval into 'n' segments; default 1
removeoutliers	remove PSDs that fall outside the station noise baseline; default 1
ymax		mcompute HVSR using method (see above); default 4
showplot	turn plot display on/off default is 1 (plot file is generated for both options)



EXAMPLES:

getStationChannelBaseline.py net=IU sta=ANMO loc=00 chan=BHZ start=2002-11-20 end=2008-11-20 plot=1 plotnnm=1 verbose=1 percentlow=10 percenthigh=90

getStationChannelBaseline.py net=TA sta=TCOL loc=-- chan=BHZ,BHN,BHE start=2013-01-01 end=2014-01-01 plot=1 plotnnm=1 verbose=1 percentlow=10 percenthigh=90

computeHVSR.py net=TA sta=TCOL loc=-- chan=BHZ,BHN,BHE start=2013-01-01 end=2013-01-01 plot=1 plotbad=0 plotpsd=0 plotpdf=1 verbose=1 ymax=5 xtype=frequency n=1 removeoutliers=0 method=4

computeHVSR.py net=TA sta=TCOL loc=-- chan=BHZ,BHN,BHE start=2013-01-01 end=2013-02-01 plot=1 plotbad=0 plotpsd=0 plotpdf=1 verbose=1 ymax=5 xtype=frequency n=1 removeoutliers=1 method=4

computeHVSR.py net=TA sta=M22K loc= chan=BHZ,BHN,BHE start=2017-01-01 end=2017-02-01 plot=1 plotbad=0 plotpsd=0 plotpdf=1 verbose=1 ymax=6 xtype=frequency n=1 removeoutliers=0 method=4

computeHVSR.py net=TA sta=E25K loc= chan=BHZ,BHN,BHE start=2017-01-01 end=2017-02-01 plot=1 plotbad=0 plotpsd=0 plotpdf=1 verbose=1 ymax=5 xtype=frequency n=1 removeoutliers=0 method=4

computeHVSR.py net=TA sta=E25K loc= chan=BHZ,BHN,BHE start=2017-07-01 end=2017-08-01 plot=1 plotbad=0 plotpsd=0 plotpdf=1 verbose=1 ymax=5 xtype=frequency n=1 removeoutliers=0 method=4


CITATION:

To cite the use of this software please cite:

Manochehr Bahavar, Zack J. Spica, Francisco J. Sánchez‐Sesma, Chad Trabant, Arash Zandieh, Gabriel Toro; Horizontal‐to‐Vertical Spectral Ratio (HVSR) IRIS Station Toolbox. Seismological Research Letters doi: https://doi.org/10.1785/0220200047

Or cite the following DOI:
    10.17611/dp/hvsrtool.1

REFERENCES:

Albarello, Dario & Lunedei, Enrico. (2013). Combining horizontal ambient vibration components for H/V 
	spectral ratio estimates. Geophysical Journal International. 194. 936-951. 10.1093/gji/ggt130.

Francisco J Sanchez-Sesma, Francisco & Rodriguez, Miguel & Iturraran-Viveros, Ursula & Luzon, Francisco & Campillo, Michel & Margerin, Ludovic & Garcia-Jerez, Antonio & Suarez, Martha & Santoyo, Miguel & Rodriguez-Castellanos, A. (2011). A theory for microtremor H/V spectral ratio: Application for a layered medium. Geophysical Journal International. 186. 221-225. 10.1111/j.1365-246X.2011.05064.x.

Peterson, J. (1993). Observations and modeling of seismic background noise, U.S. Geological Survey
	open-file report (Vol. 93-322, p. 94). Albuquerque: U.S. Geological Survey.

Guidelines for the Implementation of the H/V Spectral Ratio Technique on Ambient Vibrations, December
	2004  Project No. EVG1-CT-2000-00026 SESAME.
		ftp://ftp.geo.uib.no/pub/seismo/SOFTWARE/SESAME/USER-GUIDELINES/SESAME-HV-User-Guidelines.pdf



 HISTORY
    - 2023-12-19 Release R.1.1 -- References updated
    - 2020-02-24 Release R.1.1
    - 2019-07-31 Release R.1.0
    - 2018-07-10 prerelease V.2018.191
    - 2017-11-28 computeHVSR V.2017.332
    - 2017-11-16 initial version V.2017.320

 COMMENTS/QUESTIONS:

    Please contact data-help@earthscopeconsortium.atlassian.net

