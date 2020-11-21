#!/bin/sh -f

./script/fake.py -e 100 -x xcm/crab_nebula.xcm -o crab_100s_ninja_2gmc_whole_191224 --ymax 800.0

./script/fake.py -e 20 -x xcm/scox1_NB1_spec_mo.xcm -o scox1_20s_ninja_2gmc_whole_191224 --ymax 800.0

./script/fake.py -e 2000 -x xcm/crab_nebula_10mCrab.xcm -o 1mcrab_2ks_ninja_2gmc_whole_191224 --ymax 800.0

