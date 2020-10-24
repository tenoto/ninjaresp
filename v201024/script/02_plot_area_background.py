#!/usr/bin/env python

import os

cmd = "mkdir -p ninjaresp_201024/plot"
print(cmd);os.system(cmd)


## Effective area 

cmd = """
rm -f ninja_2gmc_whole_191224_area.{qdp,pco}
xspec <<EOF
data 1 ninjaresp_201024/ninja_empty.pi
resp ninjaresp_201024/ninja_2gmc_whole_191224.rmf
cpd /xw
plot effi
ipl effi
we ninja_2gmc_whole_191224_area
exit
exit
EOF
"""
print(cmd);os.system(cmd)

cmd = """
rm -f ninja_2gmc_inner_191224.{qdp,pco}
xspec <<EOF
data 1 ninjaresp_201024/ninja_empty.pi
resp ninjaresp_201024/ninja_2gmc_inner_191224.rmf
cpd /xw
plot effi
ipl effi
we ninja_2gmc_inner_191224_area
exit
exit
EOF
"""
print(cmd);os.system(cmd)

dump = """SKIP SING
CSIZ  1.20
LAB  POS Y  2.30
LAB  ROT
LWIDTH   4.
TIME OFF
COL 1 ON 2
LS    2 ON   2
LOC  0 0 1 1
LAB  F
LAB  X  Energy (keV)
LAB  Y  Effective area (cm\\u2\\d)
R    Y   0 42
R    X   0.800000012 100
LOG  X ON 1
"""
f = open("ninja_2gmc_2cases_191224_area.pco","w")
f.write(dump)
f.close()

cmd ="""
echo "@ninja_2gmc_2cases_191224_area.pco" > ninja_2gmc_2cases_191224_area.qdp
echo "!" >> ninja_2gmc_2cases_191224_area.qdp
awk '(NR>2){print }' ninja_2gmc_whole_191224_area.qdp >> ninja_2gmc_2cases_191224_area.qdp
echo "no no" >> ninja_2gmc_2cases_191224_area.qdp
awk '(NR>2){print }' ninja_2gmc_inner_191224_area.qdp >> ninja_2gmc_2cases_191224_area.qdp

qdp ninja_2gmc_2cases_191224_area.qdp <<EOF
/xw
plot 
hard ninja_2gmc_2cases_191224_area.ps/cps
exit
EOF
ps2pdf ninja_2gmc_2cases_191224_area.ps
rm -f ninja_2gmc_2cases_191224_area.ps

mv ninja_2gmc_*_191224_area.{qdp,pco} ninjaresp_201024/plot
mv ninja_2gmc_2cases_191224_area.pdf ninjaresp_201024/plot/
"""
print(cmd);os.system(cmd)



## Background --- 

dump = """
SKIP SING
CSIZ  1.20
LAB  POS Y  2.60
LAB  ROT
LWIDTH   5.
TIME OFF
COL  OFF 4 6
COL 4 ON 1
COL 6 ON 3
COL 8 ON 5
LIne ON    1
LS    2 ON   1
LW   5.0 ON   1
MArk    1 ON   1
LIne ON    2
LW   5.0 ON   2
LIne ON    3
LS    3 ON   3
LW   5.0 ON   3
MArk    1 ON   3
LIne Step    4
LW   5.0 ON   4
LIne ON    5
LS    2 ON   5
LW   5.0 ON   5
MArk    1 ON   5
LIne Step    6
LW   5.0 ON   6
LOC  0 0 1 1
LAB  F
LAB  X  Energy (keV)
LAB  Y  Counts s\\u-1\\d keV\\u-1\\d
R    X1 0.699999988 100
R    Y   1.00000005E-3 50
LOG  X ON 1
LOG  Y ON 1
"""
f = open("ninjaresp_201024/plot/ninja_2gmc_whole_crab_bgd.pco","w")
f.write(dump)
f.close()


cmd = """
xspec <<EOF
data 1 ninjaresp_201024/ninja_2gmc_whole_nxbcxb_200928.pi 
resp 1 ninjaresp_201024/ninja_2gmc_whole_191224.rmf 
data 2 ninjaresp_201024/ninja_2gmc_whole_maxinxb_200928.pi 
resp 2 ninjaresp_201024/ninja_2gmc_whole_191224.rmf 
data 3 ninjaresp_201024/ninja_2gmc_whole_simcxb_200624.pi 
resp 3 ninjaresp_201024/ninja_2gmc_whole_191224.rmf 
cpd /xw
setplot energy 
@../xcm/crab_nebula.xcm 
ipl ld
@ninjaresp_201024/plot/ninja_2gmc_whole_crab_bgd.pco
la t 
error off 1,2,3,4,5,6,7
hard ninja_2gmc_whole_crab_bgd.ps/cps
exit
exit
EOF
ps2pdf ninja_2gmc_whole_crab_bgd.ps 
rm -f ninja_2gmc_whole_crab_bgd.ps
mv ninja_2gmc_whole_crab_bgd.pdf ninjaresp_201024/plot
"""
print(cmd);os.system(cmd)





