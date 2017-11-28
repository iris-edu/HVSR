 Incorporated Research Institutions for Seismology (IRIS)
 Data Management Center (DMC)
 Data Products Team
 horizontal to vertical spectral ratio (HVSR)

 2017-11-16

----------------------------------------------------------------------------------------------------------------------------------------

 DESCRIPTION:

 The horizontal to vertical spectral ratio (HVSR) of ambient noise provides information on the fundamental natural frequency of the local sediments when
 there is a large acoustic impedance contrast between sediments and underlying rocks.

 This IRIS DMC Python script bundle provides tools to compute and plot horizontal to vertical spectral ratio (HVSR) curves using MUSTANG PDF-PSD web service.
 The bundle contains 2 Python scripts: 

   - computeStationChannelBaseline.py is a Python script that uses MUSTANG's noise-pdf (http://service.iris.edu/mustang/) web service to 
     compute channel-specific noise-baseline for a given station (McNamara et al., 2009). The resulting baseline represents the long-term PSD PDF 
     characteristics of the station-channel pair in the form of median, lower and higher percentiles of the available PSDs for the station.

   - computeHVSR.py - is a Python script that uses IRIS DMC's MUSTANG noise-psd/pdf web services (http://service.iris.edu/mustang/) to 
     compute horizontal-to-vertical spectral ratio (HVSR) for a given station, after removing PSDs that fall outside the station noise baseline
     computed by computeStationChannelBaseline.py.

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
   
   bin/computeStationChannelBaseline.py
       Call the script and provide the run arguments. By defining a parameter on the command line, user overrides the values defined for that parameter in the parameter file. 
       The call should have the form:

             getStationChannelBaseline.py net=netName sta=staName loc=locCode {chan=chanCode} start=2007-03-19 end=2008-10-28 {plot=[0,1] verbose=[0,1] percentlow=[10] percenthigh=[90] xtype=[period,frequency]}
         
             Note:
       
             the default values for the parameters between {} may be provided in the parameter file
 
   bin/computeHVSR.py
       Call the script and provide the run arguments. By defining a parameter on the command line, user overrides the values defined for that parameter in the parameter file.
       The call should have the form:

              network station location channel list     start date       end date  plot(1/0) plot      plot accepted     verbose    y-axis x-axis type     break start-end
                  |       |       |    |                |                 |             | rejected     accepted    plot  output(1/0)  max      |           interval into "n"
                  |       |       |    |                |                 |             |   PSDs(1/0)   PSDs(1/0)  PDFs(1/0) |         |       |              | segments
                  |       |       |    |                |                 |             |       |         |        |         |         |       |              |
   computeHVSR.py net=TA sta=TCOL loc= chan=BHZ,BHN,BHE start=2013-01-01 end=2013-01-01 plot=1 plotbad=0 plotpsd=0 plotpdf=1 verbose=1 ymax=5 xtype=frequency n=1

             Note:

             any parameter given on the command line will override the one defined in the parameter file


EXAMPLES:


             getStationChannelBaseline.py net=IU sta=ANMO loc=00 chan=BHZ,BH1,BH2 start=2002-11-19 end=2008-11-13 plot=1 verbose=0 percentlow=10 percenthigh=90
             getStationChannelBaseline.py net=IU sta=ANMO loc=00 start=2002-11-19 end=2008-11-13 plot=1
             getStationChannelBaseline.py net=IU sta=ANMO loc=00 chan=BH1 start=2002-11-19 end=2008-11-13 plot=1

             computeHVSR.py net=IU sta=ANMO loc=00 chan=BHZ,BH1,BH2 start=2007-05-01 end=2007-06-01 plot=1 verbose=1 ylim=5
             bin/computeHVSR.py net=UW sta=RATT loc= chan=BHZ,BHN,BHE start=2014-01-01 end=2017-01-01 plot=1 plotbad=0 plotpsd=0 plotpdf=1 verbose=0 ylim=5 xtype=frequency n=20

REFERENCES:

McNamara D.E., C.R. Hutt, L.S. Gee, H.M. Benz, and R.P. Buland, 2009, A method to establish seismic noise baselines for automated station assessment, Seismological Research Letters Jul 2009, 80 (4) 628-637; 
DOI: 10.1785/gssrl.80.4.628.  http://srl.geoscienceworld.org/content/gssrl/80/4/628.full.pdf

Guidelines for the Implementation of the H/V Spectral Ratio Technique on Ambient Vibrations, December 2004
SESAME European research project WP12 – Deliverable D23.12, European Commission – Research General Directorate
Project No. EVG1-CT-2000-00026 SESAME.
ftp://ftp.geo.uib.no/pub/seismo/SOFTWARE/SESAME/USER-GUIDELINES/SESAME-HV-User-Guidelines.pdf


 HISTORY
    - 2017-11-28: release of computeHVSR R.2017332
    - 2017-11-16: initial release R.2017320
 
 COMMENTS/QUESTIONS:

    Please contact manoch@iris.washington.edu
