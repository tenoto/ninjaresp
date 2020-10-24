#!/usr/bin/env python

import os
import argparse

__author__ = 'Teruaki Enoto'
__version__ = '0.01'

def get_parser():
	"""
	Creates a new argument parser.
	"""
	parser = argparse.ArgumentParser('fake.py',
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="""
generate fakeit simultated X-ray spectrum
		"""
		)
	version = '%(prog)s ' + __version__
	parser.add_argument('--version', '-v', action='version', version=version,
		help='show version of this command.')
	parser.add_argument('--exp', '-e', type=str, required=True, 
		help='exposure (sec).')	
	parser.add_argument('--xcm', '-x', type=str, required=True, 
		help='xcm file.')		
	parser.add_argument('--outname', '-o', type=str, required=True, 
		help='output phafile name.')		
	parser.add_argument('--bkg', type=str, required=False, 
		default='v201024/ninjaresp_201024/ninja_2gmc_whole_nxbcxb_200928.pi',
		help='background spectrum.')
	parser.add_argument('--rmf', type=str, required=False, 
		default='v201024/ninjaresp_201024/ninja_2gmc_whole_191224.rmf',
		help='response file.')
	parser.add_argument('--outdir', type=str, required=False, 
		default='out/v201024',
		help='output directory')	
	parser.add_argument('--rebin_sigma', type=int, required=False, 
		default=3,
		help='rebin_sigma')		
	parser.add_argument('--rebin_maxbin', type=int, required=False, 
		default=100,
		help='rebin_maxbin')			
	parser.add_argument('--ymax', type=float, required=False, 
		default=50.0,
		help='rebin_maxbin')	
	return parser

def generate_faked_phafiles(bkg,rmf,exp,xcm,outname,outdir,rebin_sigma=3,rebin_maxbin=100,ymax=50.):

	print(bkg,rmf,exp,xcm)

	if not os.path.exists(outdir):
		cmd = "mkdir -p %s" % outdir
		print(cmd);os.system(cmd)

	cmd  = "rm -f %s/%s.*" % (outdir,outname)
	print(cmd);os.system(cmd)

	cmd  = "xspec <<EOF\n"
	cmd += "data 1 %s\n" % bkg
	cmd += "back 1 %s\n" % bkg	
	cmd += "resp 1 %s\n" % rmf
	cmd += "setplot energy\n" 
	cmd += "@%s\n" % xcm
	cmd += "fakeit\n"
	cmd += "y\n"
	cmd += "\n"
	cmd += "%s.fak\n" % outname
	cmd += "%.1f\n" % float(exp)
	cmd += "setplot rebin %d %d\n" % (rebin_sigma,rebin_maxbin)	
	cmd += "data 2 %s\n" % bkg
	cmd += "resp 2 %s\n" % rmf	
	cmd += "ipl ld\n"
	cmd += "r x 0.7 100\n"
	cmd += "r y 1e-3 %.1f\n" % ymax
	cmd += "lwid 5\n"
	cmd += "lwid 5 on 1..100\n"
	cmd += "time off\n"
	cmd += "la t\n"
	cmd += "lab y Counts s\\u-1\\d keV\\u-1\\d\n"
	cmd += "csize 1.2\n"
	cmd += "lab rotate\n"
	cmd += "lab pos y 2.8\n"
	cmd += "col 14 on 3\n"
	cmd += "err off 3\n"
	cmd += "line on 3\n"
	cmd += "ls 2 on 3\n"
	cmd += "we %s\n" % outname
	cmd += "hard %s.ps/cps\n" % outname
	cmd += "exit\n"
	cmd += "exit\n"
	cmd += "EOF\n"
	cmd += "ps2pdf %s.ps\n" % outname
	cmd += "rm -f %s.ps\n" % outname
	cmd += "mv %s.* %s" % (outname,outdir)
	cmd += "mv %s_bkg.* %s" % (outname,outdir)
	print(cmd);os.system(cmd)

	f = open('%s/%s.xcm' % (outdir,outname),'w')
	dump = "data 1 %s/%s.fak\n" % (outdir,outname)
	dump += "resp 1 %s\n" % (rmf)
	dump += "back 1 %s\n" % (bkg)
	dump += "@%s\n" % xcm
	dump += "setplot rebin %d %d\n" % (rebin_sigma,rebin_maxbin)	
	f.write(dump)
	f.close()

def main(args=None):
	parser = get_parser()
	args = parser.parse_args(args)

	generate_faked_phafiles(args.bkg,args.rmf,args.exp,args.xcm,
		args.outname,args.outdir,args.rebin_sigma,args.rebin_maxbin,args.ymax)

if __name__=="__main__":
	main()


