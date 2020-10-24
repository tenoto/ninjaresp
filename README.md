# NinjaSat GMC Response (ninjaresp)

https://github.com/tenoto/ninjaresp.git


# Latest response files (v201024)

- Original response files
Whole = inner + outer: https://drive.google.com/file/d/1iXHol6E_iB3P1Phf9_E1su3adgNbpioM/view
Inner pad only: https://drive.google.com/file/d/1BoACrQcTa6zcoUwQ5XZF9JyjBJExPWGw/view

- Be window included
- aperture fraction: 73.5% (collimator, ideal) 
- aperture fraction: 71% (Be window support windw)
- total: 0.52185

- Simulated CXB spectrum: ninja_1gmc_whole_simcxb_200624.pi
	- original file SimCXB_200624.pi (see ninjasat:00939) was renamed 
	- 'INSTRUME' keyword is reset to '1GMC'
	- Earth occultation considered
	- EO fraction: 0.65566 = 1.0 - cos(asin(6371/(6371+415)))
	- Inner and outer electrodes used
	- No anti-coincidence
	- No pulse shape discrimination
	- Intrinsic detector FWHM = 20%/sqrt(E/[5.9 keV])
	- Electrical noise = 0.1 keV in sigma

see (cubesat:00165) 


# Xspec XCM files 

xcm/crab_nebula.xcm           xcm/scox1_NB1_spec_mo.xcm
xcm/crab_xmm_fixed_model.xcm

# Change history

2020-10-24: First upload (T.Enoto)


![NinjaSat Emblem](https://github.com/tenoto/repository/blob/master/ninjasat/emblem/png/ninjasat_emblem-400px.png)