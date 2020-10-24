# NinjaSat GMC Response (ninjaresp)

https://github.com/tenoto/ninjaresp.git

# Latest response files (v201024)

- all the files are stored in v201024/ninjaresp_201024/
	- usage: git clone https://github.com/tenoto/ninjaresp.git
	- ninja_?gmc_whole/inner_xxxxx_200928
		- ? = 1 or 2 
		- whole or inner 
		- xxxxx : file information 

- ninja_2gmc_whole_191224.rmf (default response)
    - sum of 2 GMCs, 'INSTRUME' keyword is reset to '2GMC'
    - sum of the inner and outer readout pads (whole)
    - thickness of the sensitive volume 1.62 cm (see cubesat:00165), which should be 1.545 cm at the latest design of the EM model
    - scirpts to make these files are also included.
	- absorption by the Be window is included
	- aperture fraction 69% is included (measured at the EM model, note. 73.5% for ideal)
	- aperture fraction 71% is included (Be window supporting entrance window)
	- Original response files (see cubesat:00165):
	    - [CubeSatGasDetWhole.rmf](https://riken-share.box.com/shared/static/0udo2hmm91tap2qiulgsc8gx2jganpwv.rmf): whole = inner + outer (cubesat:00165)
	    - [CubeSatGasDetInner.rmf](https://riken-share.box.com/shared/static/ovrk6q48l7ktkp6p97gkrqxpe49r6zzh.rmf): inner pad only, created (cubesat:00165), appling the anti-coincidence for events with >1 keV at the outer pad

- ninja_2gmc_whole_nxbcxb_200928.pi
	- used as the default backgroudn file 
	- ninja_2gmc_whole_simcxb_200624.pi + ninja_2gmc_whole_maxinxb_200928.pi

- ninja_2gmc_whole_simcxb_200624.pi 
	- simulated CXB spectrum
	- ninjasat:00939 as the original file SimCXB_200624.pi (renamed)
	- 'INSTRUME' keyword is reset to '2GMC', and count is doubled for 2 GMCs.
	- Earth occultation considered
	- EO fraction: 0.65566 = 1.0 - cos(asin(6371/(6371+415)))
	- Inner and outer electrodes used
	- No anti-coincidence
	- No pulse shape discrimination
	- Intrinsic detector FWHM = 20%/sqrt(E/[5.9 keV])
	- Electrical noise = 0.1 keV in sigma

- ninja_2gmc_whole_maxinxb_200928.pi
	- assumed NXB spectrum just normalized from MAXI
	- CXB contribution is excluded.
    - (ninjasat:01358) the original file ninja_simnxb_200928.csv

- ninja_empty.pi
 	- empty pha file for Xspec fake, created
 	- original file name "empty.pi"

- References (link to the internal-only webpage)
    - [Be window attenuation](https://astro.riken.jp/gwxwiki/lib/exe/fetch.php?media=transmission_be_20200711.pdf)
    - [Effective area evaluation by Takeda and Sato](https://astro.riken.jp/gwxwiki/lib/exe/fetch.php?media=gmc_effective_area.pdf)

- []()

[effective area]()

# Xspec XCM files 

- crab_nebula.xcm 
- crab_xmm_fixed_model.xcm 
- scox1_NB1_spec_mo.xcm (Sasaki, master thesis, Osaka University, 2014)

# Change history

2020-10-24: First upload (T.Enoto)

![NinjaSat Emblem](https://github.com/tenoto/repository/blob/master/ninjasat/emblem/png/ninjasat_emblem-400px.png)





