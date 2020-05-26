# Things that turned out to be not as easy as initially imagined

## Fmask
- only installable via conda
- Permitting Grass to find conda-python interpreter but still running grass didn't work
	+ we tried modidyfing PATH, PYTHONPATH, GRASS_PYTHOn
	+ We created symlinks with link to the conda interpreter and put the mother-directory on GRASS_PYTHON
	+ We tried to install `fmask` from source and put it to some place where python always would find it
	+ GRASS didn't find it when running `import fmask`
	+ We put the python-script in the directory where fmask comes from as when executing a python-script from within GRASS, this directory is always added to some Variable that GRASS should find. Caused Problems with numpy installation
- the output of fmask is not in the same size as the input which complicates masking the clouds afterwards

## Atmospheric Correction
- super time consuming
- `sen2cor` only works on uncropped L1C-Data (which are gigantic)
- 

## Mering
