#!/usr/bin/env python

import os 
import pandas as pd
import astropy.io.fits as fits

## Remname -----

cmd = """
rm -rf ninjaresp_201024
mkdir -p ninjaresp_201024/tmp

cp raw/CubeSatGasDetInner.rmf ninjaresp_201024/tmp/ninja_1gmc_inner_woaperture_191224.rmf
cp raw/CubeSatGasDetWhole.rmf ninjaresp_201024/tmp/ninja_1gmc_whole_woaperture_191224.rmf

cp raw/empty.pi ninjaresp_201024/ninja_empty.pi
cp raw/SimCXB_200624.pi ninjaresp_201024/ninja_1gmc_whole_simcxb_200624.pi
"""
print(cmd);os.system(cmd)


## Set header keywords -----

rmf_file_list = [
	"ninjaresp_201024/tmp/ninja_1gmc_inner_woaperture_191224.rmf",
	"ninjaresp_201024/tmp/ninja_1gmc_whole_woaperture_191224.rmf"
	]
for file in rmf_file_list:
	for extension in [0,1,2]:
		cmd  = "fparkey '1GMC' %s[%d] 'INSTRUME'\n" % (file,extension)
		cmd += "fparkey 'NinjaSat' %s[%d] 'TELESCOP'\n" % (file,extension)
		print(cmd);os.system(cmd)

pi_file_list = [
	"ninjaresp_201024/ninja_empty.pi",
	"ninjaresp_201024/ninja_1gmc_whole_simcxb_200624.pi"
	]
for file in pi_file_list:
	for extension in [0,1]:
		cmd  = "fparkey '1GMC' %s[%d] 'INSTRUME'\n" % (file,extension)
		cmd += "fparkey 'NinjaSat' %s[%d] 'TELESCOP'\n" % (file,extension)
		print(cmd);os.system(cmd)		


## sum rmf into 2GMC ----

# see (cubesat:00165) 
# whole: https://drive.google.com/file/d/1iXHol6E_iB3P1Phf9_E1su3adgNbpioM/view
# Inner pad only: https://drive.google.com/file/d/1BoACrQcTa6zcoUwQ5XZF9JyjBJExPWGw/view

# Be window included
# aperture fraction: 73.5% (collimator, ideal) 
# aperture fraction: 69% (collimator, EM measured)
# aperture fraction: 71% (Be window support windw)
#- total: 0.4899

#	"ninjaresp_201024/ninja_1gmc_inner_woaperture_191224.rmf",
#	"ninjaresp_201024/ninja_1gmc_whole_woaperture_191224.rmf"

for padtype in ["whole","inner"]:
	f = open('ninjaresp_201024/tmp/ninja_1gmc_%s_191224.list' % padtype,'w')
	f.write('ninjaresp_201024/tmp/ninja_1gmc_%s_woaperture_191224.rmf 0.4899\n' % padtype)
	f.write('ninjaresp_201024/tmp/ninja_1gmc_%s_woaperture_191224.rmf 0.0\n' % padtype)
	f.close()

	cmd = """
rm -f ninjaresp_201024/ninja_1gmc_%s_191224.rmf
addrmf @ninjaresp_201024/tmp/ninja_1gmc_%s_191224.list <<EOF
ninjaresp_201024/ninja_1gmc_%s_191224.rmf
EOF
""" % (padtype,padtype,padtype)
	print(cmd);os.system(cmd)


for padtype in ["whole","inner"]:
	f = open('ninjaresp_201024/tmp/ninja_2gmc_%s_191224.list' % padtype,'w')
	f.write('ninjaresp_201024/tmp/ninja_1gmc_%s_woaperture_191224.rmf 0.4899\n' % padtype)
	f.write('ninjaresp_201024/tmp/ninja_1gmc_%s_woaperture_191224.rmf 0.4899\n' % padtype)
	f.close()

	cmd = """
rm -f ninjaresp_201024/ninja_2gmc_%s_191224.rmf
addrmf @ninjaresp_201024/tmp/ninja_2gmc_%s_191224.list <<EOF
ninjaresp_201024/ninja_2gmc_%s_191224.rmf
EOF
""" % (padtype,padtype,padtype)
	print(cmd);os.system(cmd)

	rmffile = "ninjaresp_201024/ninja_2gmc_%s_191224.rmf" % padtype 
	for extension in [0,1,2]:
		cmd  = "fparkey '2GMC' %s[%d] 'INSTRUME'\n" % (rmffile,extension)
		print(cmd);os.system(cmd)


## NXB file conversion to pi file -----

cmd = "rm -f ninjaresp_201024/ninja_1gmc_whole_maxinxb_200928.pi"
print(cmd);os.system(cmd)

df_nxb_1gmc = pd.read_csv("raw/ninja_simnxb_200928.csv",skiprows=6,header=0)
exposure = 1000000.0
energy_binsize = 0.1
cnts_nxb_1gmc = (df_nxb_1gmc[" counts/s/keV"]*exposure*energy_binsize).astype(int)

hdu_cxb_1gmc = fits.open("ninjaresp_201024/ninja_1gmc_whole_simcxb_200624.pi")
#print(hdu_cxb_1gmc["SPECTRUM"].data["COUNTS"])

for i in range(len(hdu_cxb_1gmc["SPECTRUM"].data["COUNTS"])):
	hdu_cxb_1gmc["SPECTRUM"].data["COUNTS"][i] = cnts_nxb_1gmc[i]

#print(hdu_cxb_1gmc["SPECTRUM"].data["COUNTS"])
hdu_cxb_1gmc.writeto('ninjaresp_201024/ninja_1gmc_whole_maxinxb_200928.pi')


## add NXB + CXB ------

cmd = "rm -f ninjaresp_201024/ninja_1gmc_whole_nxbcxb_200928.pi"
print(cmd);os.system(cmd)

hdu_cxb_1gmc = fits.open("ninjaresp_201024/ninja_1gmc_whole_simcxb_200624.pi")
#print(hdu_cxb_1gmc["SPECTRUM"].data["COUNTS"])

for i in range(len(hdu_cxb_1gmc["SPECTRUM"].data["COUNTS"])):
	hdu_cxb_1gmc["SPECTRUM"].data["COUNTS"][i] += cnts_nxb_1gmc[i]

#print(hdu_cxb_1gmc["SPECTRUM"].data["COUNTS"])
hdu_cxb_1gmc.writeto('ninjaresp_201024/ninja_1gmc_whole_nxbcxb_200928.pi')


## 1GMC to 2GMC

for datatype in ["maxinxb_200928","simcxb_200624","nxbcxb_200928"]:
	infile = "ninjaresp_201024/ninja_1gmc_whole_%s.pi" % datatype
	outfile = "ninjaresp_201024/ninja_2gmc_whole_%s.pi" % datatype

	cmd = "rm -f %s" % outfile
	print(cmd);os.system(cmd)

	hdu_1gmc = fits.open(infile)
	hdu_1gmc["SPECTRUM"].data["COUNTS"] = 2 * hdu_1gmc["SPECTRUM"].data["COUNTS"]
	hdu_1gmc.writeto(outfile)

	for extension in [0,1]:
		cmd  = "fparkey '2GMC' %s[%d] 'INSTRUME'\n" % (outfile,extension)
		print(cmd);os.system(cmd)






