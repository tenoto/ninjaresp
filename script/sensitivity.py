#!/usr/bin/env python

import os
import argparse
import pandas as pd
import numpy as np

__author__ = 'Teruaki Enoto'
__version__ = '0.01'

# 1 Crab ~ 2.3e-8 erg/s/cm2 (2-10 keV)
# 1 eV = 1.60e-12 erg
# 1 keV = 1.60e-9 erg

def get_parser():
	"""
	Creates a new argument parser.
	"""
	parser = argparse.ArgumentParser('sensitivity.py',
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="""
sensivtivity calculation
		"""
		)
	version = '%(prog)s ' + __version__
	parser.add_argument('--version', '-v', action='version', version=version,
		help='show version of this command')
	parser.add_argument('--exp', '-e', type=float, required=True, 
		help='exposure (sec)')	
	parser.add_argument('--emin', type=float, required=True, 
		help='energy min (keV)')		
	parser.add_argument('--emax', type=float, required=True, 
		help='energy max (keV)')		
	parser.add_argument('--bkg', type=str, required=False, 
		default='v201024/ninjaresp_201024/ninja_2gmc_whole_maxinxb_200928',
		help='background spectrum.')
	parser.add_argument('--rmf', type=str, required=False, 
		default='v201024/ninjaresp_201024/plot/ninja_2gmc_whole_191224_area.qdp',
		help='response file (qdp format).')
	return parser

def calc_sensitivity(bkg,rmf,exp,emin,emax):

	print(bkg,rmf,exp,emin,emax)

	df_rmf = pd.read_csv(rmf,skiprows=2,names=["keV","cm2"],delimiter=" ")

	flag_eband = np.logical_and(df_rmf["keV"] >= emin, df_rmf["keV"] <= emax)
	average_cm2 = np.average(df_rmf["cm2"][flag_eband])

	width_eband = emax - emin 
	print("Emin: %.3f keV" % emin)
	print("Emax: %.3f keV" % emax)	
	print("Energy band width: %.3f keV" % width_eband)
	print("Band-average area: %.3f cm2" % average_cm2)
	average_keV = np.average(df_rmf["keV"][flag_eband])
	print("Average energy: %.3f keV" % average_keV)

	print("Exposure: %.3f sec" % exp)
	Fmin_photonlimit = 3.0**2 / average_cm2 / exp / width_eband
	Fmin_photonlimit_erg = Fmin_photonlimit * width_eband * average_keV * 1.60e-9
	print("--------------")
	print("Photon limit Fmin: %.3e photons/s/cm2/keV (%.1f-%.1f keV, %.3f ks)" % (Fmin_photonlimit,emin,emax,exp/1000))
	print("Photon limit Fmin: %.3e erg/s/cm2" % (Fmin_photonlimit_erg))
	# Idesawa, Master thesis, Eq (A.10) 
	print("--------------")


def main(args=None):
	parser = get_parser()
	args = parser.parse_args(args)

	calc_sensitivity(args.bkg,args.rmf,args.exp,args.emin,args.emax)

if __name__=="__main__":
	main()







