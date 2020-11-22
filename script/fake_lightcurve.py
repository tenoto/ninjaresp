#!/usr/bin/env python

import os
import numpy as np 
import argparse
import astropy.io.fits as fits
import matplotlib.pyplot as plt

__author__ = 'Teruaki Enoto'
__version__ = '0.01'

def get_parser():
	"""
	Creates a new argument parser.
	"""
	parser = argparse.ArgumentParser('fake_lightcurve.py',
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="""
download nicer mkf file.
		"""
		)
	version = '%(prog)s ' + __version__
	parser.add_argument('--version', '-v', action='version', version=version,
		help='show version of this command.')
	parser.add_argument('--obsid', '-o', type=str, required=True, 
		help='obsid.')	
	parser.add_argument('--yyyymm', '-y', type=str, required=True, 
		help='yyyymm.')		
	parser.add_argument('--bin', '-b', type=int, required=True, 
		help='binning time (sec) [integer].')	
	parser.add_argument('--xmin', type=int, required=False, 
		default=-99,help='time min')			
	parser.add_argument('--xmax', type=int, required=False, 
		default=-99,help='time max')	
	parser.add_argument('--ninja', type=float, required=False, 
		default=-99,help='Ninja count rate')								
	return parser

def wget_nicer_mkf(obsid,yyyymm):
	yyyy_mm = yyyymm[0:4] + '_' + yyyymm[4:6]

	obsid_path = 'https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/%s/%s' % (yyyy_mm,obsid)
	mkffile_path = '%s/auxil/ni%s.mkf.gz' % (obsid_path,obsid); 
	mkffile = os.path.basename(mkffile_path)
	cmd = 'wget -q -nH --no-check-certificate --cut-dirs=8 -r -l0 -c -N -np -R \'index*\' -erobots=off --retr-symlinks %s;' % mkffile_path
	print(cmd);os.system(cmd)

def plot_curve(mkffile,bin,xmin,xmax,ninja_rate,obsid):
	"""
	     62 TOT_XRAY_COUNT             1J
	"""
	print(mkffile)
	hdu = fits.open(mkffile)
	time_series = hdu[1].data['TIME'] - hdu[1].data['TIME'][0]
	cnt_series = hdu[1].data['TOT_XRAY_COUNT'] 
	err_series = np.sqrt(cnt_series)
	module_cnt_series = np.divide(cnt_series, hdu[1].data['NUM_FPM_ON'])
	module_err_series = np.divide(err_series, hdu[1].data['NUM_FPM_ON'])	

	if xmin < 0 or xmax < 0:
		flag_time = np.full(len(time_series), True, dtype=bool)
	else:
		flag_time = np.logical_and(time_series >= xmin, time_series <= xmax)

	x = time_series[flag_time]
	y = module_cnt_series[flag_time]
	yerr = module_err_series[flag_time]

	outpdf = mkffile.replace('mkf.gz','pdf')
	fig, axes = plt.subplots(nrows=1,ncols=1,sharex=True,figsize=(12,4))
	#plt.gca().invert_yaxis()
	plt.errorbar(x,y,yerr=yerr, marker='', drawstyle='steps-mid') 
	#plt.plot(time_series[flag_time],cnt_series[flag_time],'o-')
	axes.set_xlabel('Time (sec)');
	axes.set_ylabel('Count Rate (cps) per single NICER module')
	axes.set_xlim(xmin,xmax)
	plt.savefig(outpdf,bbox_inches='tight',transparent=True)	

	cmd = 'open %s' % outpdf
	print(cmd);os.system(cmd)

	# =======
	nicer_rate = np.nanmean(y)
	normalization = ninja_rate / nicer_rate
	print("nicer rate: %.1f (per module)" % nicer_rate)
	print("ninja rate: %.1f (two GMCs)" % ninja_rate)
	print("normalization: %.3e" % normalization)

	ninja_cnt_series = normalization * y
	ninja_err_series = np.sqrt(ninja_cnt_series)

	outpdf = outpdf.replace('ni','ninjasim')
	fig, axes = plt.subplots(nrows=1,ncols=1,sharex=True,figsize=(12,4))
	#plt.gca().invert_yaxis()
	#plt.errorbar(x,ninja_cnt_series,yerr=ninja_err_series, marker='', drawstyle='steps-mid') 
	axes.step(x-x[0],ninja_cnt_series)
	#plt.plot(x,ninja_cnt_series,marker='',drawstyle='steps-mid')
	axes.set_xlabel('Time (sec)');
	axes.set_ylabel('NinjaSat Count Rate (cps)')
	axes.set_xlim(xmin-x[0],xmax-x[0])
	plt.savefig(outpdf,bbox_inches='tight',transparent=True)	

	cmd = 'open %s' % outpdf
	print(cmd);os.system(cmd)

	cmd = 'mkdir -p out/v201024/ninjasim%s' % obsid
	print(cmd);os.system(cmd)
	cmd = 'mv *%s* out/v201024/ninjasim%s' % obsid 
	print(cmd);os.system(cmd)

def main(args=None):
	parser = get_parser()
	args = parser.parse_args(args)

	mkffile = 'ni%s.mkf.gz' % args.obsid
	if not os.path.exists(mkffile):
		wget_nicer_mkf(args.obsid,args.yyyymm)
	plot_curve(mkffile,args.bin,args.xmin,args.xmax,args.ninja,args.obsid)

if __name__=="__main__":
	main()


