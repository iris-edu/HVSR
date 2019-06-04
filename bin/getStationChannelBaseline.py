#!/usr/bin/env python

"""
 NAME: getStationChannelBaseline.py

 DESCRIPTION: A Python script that uses IRIS DMC's MUSTANG noise-pdf web service http://service.iris.edu/mustang/ to
 compute channel-specific noise-baseline for a given station. The algorithm is based on McNamara et al. (2009)

 Copyright (C) 2019  Product Team, IRIS Data Management Center

    This is a free software; you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as
    published by the Free Software Foundation; either version 3 of the
    License, or (at your option) any later version.

    This script is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License (GNU-LGPL) for more details.  The
    GNU-LGPL and further information can be found here:
    http://www.gnu.org/

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

 INPUTS: Script expects a configuration parameter file under the 'param' directory. the parameter file's name is the
 same as this scripts name with '_param' appended.

 USAGE:

 getStationChannelBaseline.py net=netName sta=staName loc=locCode {chan=chanCode} start=2007-03-19
 end=2008-10-28 {plot=[0, 1] verbose=[0, 1] percentlow=[10] percenthigh=[90] x_type=[period,frequency]}

 getStationChannelBaseline.py net=IU sta=ANMO loc=00 chan=BHZ start=2002-11-20 end=2008-11-20 plot=1
 verbose=1 percentlow=10 percenthigh=90

 the default values for the parameters between {} may be provided in the parameter file

 HISTORY:
     2019-06-03 IRIS DMC Product Team (Manoch): V.2019.154, addressed the issue with start and end dates to be the same,
                                                updated the code style, improved plotting.
     2018-07-10 IRIS DMC Product Team (Manoch): pre-release version V.2018.191
     2017-11-16 IRIS DMC Product Team (Manoch): V.2017.320
     2017-03-12 IRIS DMC Product Team (Manoch): created (V.2017.071)

 REFERENCES:
    A Method to Establish Seismic Noise Baselines for Automated Station Assessment D. E. McNamara, C. R. Hutt,
    L. S. Gee, H. M. Benz, R. P. Buland (2009)

        http://srl.geoscienceworld.org/content/80/4/628

"""

version = 'V.2019.154'

import os
import sys

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText

import numpy as np
import urllib
import datetime
import importlib

# Set paths based on the script's location.
scriptDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
script = os.path.basename(__file__)
paramPath = os.path.join(scriptDirectory, 'param')
libPath = os.path.join(scriptDirectory, 'lib')
sys.path.append(paramPath)
sys.path.append(libPath)

# Import  HVSR parameters and libraries.
import fileLib as fileLib
import msgLib as msgLib

def usage():
   """The usage message.
   """
   print('\n\n{} ({}):'.format(script, version))
   print('\nThis script uses IRIS DMC\'s MUSTANG noise-pdf web service (http://service.iris.edu/mustang/) to\n'
         'compute channel-specific noise-baseline for a given station. The algorithm is based on the paper:\n\n'
         'A Method to Establish Seismic Noise Baselines for Automated Station Assessment,\n'
         'D. E. McNamara, C. R. Hutt, L. S. Gee, H. M. Benz, R. P. Buland (2009), '
         '\nhttp://srl.geoscienceworld.org/content/80/4/628')
   print('\n\nUsage:\n{} net=netName sta=staName loc=locCode chan=chanCode\n\tstart=2007-03-19 '
         'end=2008-10-28 plot=[0, 1]'
         'verbose=[0, 1] percentlow=[10] \n\tpercenthigh=[90] xtype=[period,frequency]'.format(script))
   print('\nnet\t\tstation network code'
         '\nsta\t\tstation code'
         '\nloc\t\tstation location code'
         '\nchan\t\tstation channel code (separate multiple channel codes by comma); \n\t\tdefault: {}'
         '\nxtype\t\tX-axis  type; default: {}'
         '\nstart\t\tstart date of the interval for which station baseline is computed (format YYYY-MM-DD).'
         '\n\t\tIf time is not provided, the start day begins at 00:00:00 UTC'
         '\nend\t\tend date of the interval for which station baseline is computed (format YYYY-MM-DD).'
         '\n\n\t\tNOTE: PSD segments will be limited to those starting between start (inclusive) and '
         '\n\t\tend (exclusive) except when start and end are the same (in that case, the range will '
         '\n\t\tcover start day only).'
         '\n\nverbose\t\tRun in verbose mode to provide informative messages [0=no, 1=yes];'
         '\n\t\tdefault:{}'
         '\npercentlow\tlowest percentile to compute (float); default {}'
         '\npercenthigh\tHighest percentile to compute (float); default {}'
         .format(param.chan, param.xtype, param.verbose, param.percentlow, param.percenthigh))
   print('\n\nexample:\ngetStationChannelBaseline.py net=IU sta=ANMO loc=00 chan=BHZ start=2002-11-20 '
         'end=2008-11-20 plot=1 '
         'verbose=1 percentlow=10 percenthigh=90\n\n')

def get_args(arg_list):
   """Get the run arguments.
   """
   these_args = {}
   for this_index, this_value in enumerate(arg_list):
      if '=' not in this_value:
         continue
      key, value = this_value.split('=')
      these_args[key.strip()] = value.strip()
   return these_args


def get_param(these_args, this_key, this_value=None):
   """Get a run argument for a given key.
   """
   if this_key in these_args.keys():
      msgLib.info('{}: {}'.format(this_key, these_args[this_key]))
      return these_args[this_key]
   elif this_value is not None:
      return this_value
   else:
      msgLib.error('Missing parameter {}'.format(this_key), 1)
      usage()
      sys.exit()

# Get user-provided arguments and script libraries.
args = get_args(sys.argv)
param_file_name = '{}_param'.format(script.replace('.py', ''))

print('\n\n\n')
msgLib.info(', '.join([script,param_file_name, version]))

try:
   param = importlib.import_module(param_file_name)
except Exception as e:
   msgLib.error('failed to load: {}\n{}'.format(param_file_name, e), 1)
   sys.exit()

verbose = int(get_param(args, 'verbose', this_value=param.verbose))
do_plot = int(get_param(args, 'plot', this_value=param.plot))
if verbose:
   msgLib.info('Param Path: {}'.format(paramPath))
   msgLib.info('loaded: {}'.format(param_file_name))



# If plot is not requested, turn the display requirement.
if do_plot <= 0:
   msgLib.info('Plot OFF!')
   matplotlib.use('agg')
else:
   from obspy.imaging.cm import pqlx

channel_list = get_param(args, 'chan', this_value=param.chan)
network = get_param(args, 'net', msgLib)
if network is None:
   msgLib.error('network not defined!', 1)
   sys.exit()
station = get_param(args, 'sta', msgLib)
if station is None:
   msgLib.error('station not defined!', 1)
   sys.exit()
location = get_param(args, 'loc', msgLib)
if location == 'DASH':
   location = '--'
if location is None:
   msgLib.error('location not defined!', 1)
   sys.exit()

percent_low = get_param(args, 'percentlow', this_value=param.percentlow)
percent_mid = get_param(args, 'percentmid', this_value=param.percentmid)
percent_high = get_param(args, 'percenthigh', this_value=param.percenthigh)
percentile = [float(percent_low), float(percent_mid), float(percent_high)]
percent_plot_type = get_param(args, 'percentPlotType', this_value=param.percentPlotType)

# Get start and end dates and check for their validity.
start = get_param(args,'start').strip()
try:
   start_time = datetime.datetime.strptime(start, '%Y-%m-%d')
except Exception as e:
   msgLib.error('bad start',start)
   print(e)
   sys.exit()
   
end = get_param(args,'end',msgLib).strip()
try:
   end_time = datetime.datetime.strptime(end, '%Y-%m-%d')
   if start == end:
      end_time = end_time + datetime.timedelta(days=1)
except Exception as e:
   msgLib.error('bad end', end)
   print(e)
   sys.exit()

if end_time < start_time:
   msgLib.error('bad end value (must be >= start)', end)
   sys.exit()

x_type = get_param(args, 'xtype', this_value=param.xtype)

channel_index = -1
got_data = False
channels = channel_list.strip().replace(' ', '').split(',')
psd_count = {}
for channel in channels:
   channel_index += 1
   X = list()
   Y = list()
   P = list()
   x_values = list()
   y_values = list()
   pct_low = list()
   pct_mid = list()
   pct_high = list()

   target = '.'.join([network,station,location,channel,'M'])
   if start == end:
       title = ' '.join(['.'.join([network,station,location]),'Station-Channel Baseline for',start])
       msgLib.info('requesting {} for {}'.format(target, start))
   else:
      title = ' '.join(['.'.join([network, station, location]), 'Station-Channel Baseline', start, '-',
                        end])
      msgLib.info('requesting {} from {} to {}'.format(target, start, end))
   URL = '{}target={}&starttime={}&endtime={}&format=text'.format(
      param.mustangUrl, target, start_time.strftime('%Y-%m-%d'), end_time.strftime('%Y-%m-%d'))

   label = '.'.join([network, station, location, channel_list.replace(',','-'),'PSDs', x_type, start,
                     end])

   baseline_file_name = os.path.join(param.baselineDirectory, fileLib.baselineFileName(
      network, station, location, channel))
   baseline_file = open(baseline_file_name, 'w')
   baseline_file.write('#%s %s percentile %s percentile %s percentile\n'%(
      'frequency', percent_low, percent_mid, percent_high))


   if verbose:
      msgLib.info('requesting: {}'.format(URL))
   try:
      link = urllib.request.urlopen(URL)
   except Exception as e:
      got_data = False
      msgLib.error('failed on target {} {}'.format(target, URL), 1)
      print (e)

      continue
   
   msgLib.info('waiting for reply....')

   data = link.read().decode()
   lines = data.split('\n')
   end_frequency = ''
   got_data = True
   line_count = 0
   non_blank_last_line = 0
   if len(lines[-1].strip()) <= 0:
      non_blank_last_line = 1
   for line in lines:
      line_count += 1
      if len(line.strip()) <= 0:
         continue
      if line[0] == '#' or ',' not in line:
         continue

      (freq, power, hits) = line.split(',')
      if end_frequency == '':
         end_frequency = freq.strip()
         power_list = list()
         power_list.append(float(power.strip()))
         hits_list = list()
         hits_list.append(int(hits.strip()))
      elif end_frequency == freq.strip():
         power_list.append(float(power.strip()))
         hits_list.append(int(hits.strip()))

      # Got all the counts for this bin, find the percentiles.
      if end_frequency != freq.strip() or line_count == len(lines) - non_blank_last_line:
         totalHits = sum(hits_list)

         # Get the number of contributing PSDs from the first bin of each channel.
         if channel not in psd_count.keys():
            psd_count[channel] = totalHits

         values = list()
         y_values.append(np.array(hits_list)*100.0/totalHits)

         # Find the percentiles.
         for p in percentile:
            total = 0
            this_level = p * float(totalHits) / 100.0
            # power goes from low to high
            # here we define percentile as the smallest value in the list such that
            # no more than P percent of the data is strictly less than the value 
            # and at least P percent of the data is less than or equal to that value
            previous_power =  None
            for (currentHits, currentPower) in zip(hits_list,power_list):
               if previous_power is None:
                  previous_power = currentPower 
               total += int(currentHits)
               if float(total) == this_level:
                  values.append(currentPower)
                  break
               elif float(total) > this_level:
                  values.append(previous_power)
                  break
               previous_power = currentPower

         if x_type == 'period':
            last_x = 1.0/float(end_frequency)
            x_values.append(last_x)
         else:
            last_x = float(end_frequency)
            x_values.append(last_x)

         # Write the baseline file.
         baseline_file.write('%s %0.2f %0.2f %0.2f\n'%(end_frequency,values[0],values[1],values[2]))

         # Save values for the plot.
         for i in range(len(hits_list)):
            Y.append(float(power_list[i]))
            P.append(float(hits_list[i]) * 100.0 / float(totalHits))
            X.append(last_x)

         pct_low.append(values[0])
         pct_mid.append(values[1])
         pct_high.append(values[2])

         end_frequency = freq.strip()
         power_list = list()
         power_list.append(float(power))
         hits_list = list()
         hits_list.append(int(hits))
   msgLib.info('baseline file: {}'.format(baseline_file_name))
   baseline_file.close()

   if do_plot > 0 and got_data:

      if verbose:
          msgLib.info('PLOT Station-Channel Baseline')
      if channel_index == 0:

         fig = plt.figure(figsize=param.imageSize, facecolor='white')
         matplotlib.rcParams.update({'font.size': 6})
         fig.canvas.set_window_title(label)
         ax = list()
         ax.append(plt.subplot(len(channels), 1, channel_index+1))
      else:
         ax.append(plt.subplot(len(channels), 1, channel_index+1, sharex=ax[0]))

      cmap = pqlx

      ok = list()
      if percent_plot_type == 'line':
          plt.plot(np.array(x_values), pct_high, lw=3, c=param.colorHigh, label='{}%'.format(percent_high))
          plt.plot(np.array(x_values), pct_mid, lw=3, c=param.colorMid, label='{}%'.format(percent_mid))
          plt.plot(np.array(x_values), pct_low, lw=3, c=param.colorLow, label='{}%'.format(percent_low))
      else:
         plt.scatter(np.array(x_values), pct_high, c=param.colorHigh, s=46.5, marker='_', linewidth=param.lw * 1.5,
                     edgecolor='k',
                     alpha=1.0, zorder=200, label='{}%'.format(percent_high))
         plt.scatter(np.array(x_values), pct_mid, c=param.colorMid, s=46.5, marker='_', linewidth=param.lw * 1.5,
                     edgecolor='k',
                     alpha=1.0, zorder=200, label='{}%'.format(percent_mid))
         plt.scatter(np.array(x_values), pct_low, c=param.colorLow, s=46.5, marker='_', linewidth=param.lw * 1.5,
                     edgecolor='k',
                     alpha=1.0, zorder=200, label='{}%'.format(percent_low))

      ax[0].set_title(title)
      plt.ylabel(param.yLabel)
      plt.legend(loc='upper left')
      im = plt.scatter(X, Y, c=P, s=50, marker = '_',  linewidth=param.lw, edgecolor='face', cmap=cmap,
                       alpha=param.alpha)

      ax[channel_index].set_xscale('log')
      anchored_text = AnchoredText(' '.join(['.'.join([network, station, location, channel]),
                                             '{:,d}'.format(psd_count[channel]), 'PSDs']), loc=9)

      ax[channel_index].add_artist(anchored_text)
      plt.xlim(param.xLim[x_type])
      plt.ylim(param.yLim)
      if channel_index+1 == len(channels):
         plt.xlabel(param.xLabel[x_type])

      # Create a second axes for the colorbar.
      ax2 = fig.add_axes([0.92, 0.1, 0.01, 0.8])
      fig.colorbar(im, ax2, orientation='vertical')
      ax2.set_ylabel('Probability (%)', size=9, rotation=270, labelpad=7)
      plt.clim(param.pMin,param.pMax)

if do_plot > 0 and got_data:
   plot_fileName = os.path.join(param.imageDirectory,
                                fileLib.baselineFileName(network, station, location,
                                                           channel_list.replace(',', '-')
                                                           ).replace('.txt', '_{}.png'.format(x_type)))
   plt.savefig(plot_fileName,dpi=param.imageDpi)
   msgLib.info('Saved plot file: {}'.format(plot_fileName))
   msgLib.info('Show')
   plt.show()

print('\n\n\n')
