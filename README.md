# NinjaSat GMC Response (ninjaresp)

https://github.com/tenoto/ninjaresp.git

# Latest response files (v201024)

- Original response files (see cubesat:00165)
Whole = inner + outer: [CubeSatGasDetWhole.rmf](https://drive.google.com/file/d/1iXHol6E_iB3P1Phf9_E1su3adgNbpioM/view)
Inner pad only: [CubeSatGasDetInner.rmf](https://drive.google.com/file/d/1BoACrQcTa6zcoUwQ5XZF9JyjBJExPWGw/view)

- ninja_2gmc_whole_191224.rmf
    - use this as the default setup 
    - sum of 2 GMCs
    - sum of the inner and outer pads (whole)
    - thickness of the sensitive volume 1.62 cm (see cubesat:00165), which should be 1.545 cm at the latest design of the EM model
    - scirpts to make these files are also included.
	- Be window included
	- aperture fraction 69% (measured at the EM model, note. 73.5% for ideal)
	- aperture fraction 71% (Be window supporting entrance window)


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

# Xspec XCM files 

- crab_nebula.xcm 
- crab_xmm_fixed_model.xcm 
- scox1_NB1_spec_mo.xcm (Sasaki, master thesis, Osaka University, 2014)

# Change history

2020-10-24: First upload (T.Enoto)

![NinjaSat Emblem](https://github.com/tenoto/repository/blob/master/ninjasat/emblem/png/ninjasat_emblem-400px.png)





- [empty.pi](https://riken-share.box.com/s/drb955qhct2eiq3zri8cbyj23vo2wlse)
    - empty pha file for Xspec fake
- [SimCXB_200624.pi](https://riken-share.box.com/s/9sv7jlhduvnvonrubs8gjyp3iun3v6rq)
    - CXB simulation (ninjasat:00939)
- [NXB]
    - ninjasat:01358
- [CubeSatGasDet_wapr_2gmc_2case.pdf](https://riken-share.box.com/shared/static/0ty5p2aq5u9tpfc3ysas88wu3lcb99lg.pdf)
- Related files:
    - [CubeSatGasDetWhole.rmf](https://riken-share.box.com/shared/static/0udo2hmm91tap2qiulgsc8gx2jganpwv.rmf): created by Kitaguchi (cubesat:00165)
    - [CubeSatGasDetInner.rmf](https://riken-share.box.com/shared/static/ovrk6q48l7ktkp6p97gkrqxpe49r6zzh.rmf): created by Kitaguchi (cubesat:00165), appling the anti-coincidence for events with >1 keV at the outer pad
- References (link to the internal-only webpage)
    - [Be window attenuation](https://astro.riken.jp/gwxwiki/lib/exe/fetch.php?media=transmission_be_20200711.pdf)
    - [Effective area evaluation by Takeda and Sato](https://astro.riken.jp/gwxwiki/lib/exe/fetch.php?media=gmc_effective_area.pdf)


