# README

## Problems
-  Grass-Add-Ons with conda-package are quite difficult to implementate
- Run the script
- `fmask-python` hat high quality command line calls
-  Download conda/miniconda sets "default"-python 
-  miniconda/anaconda confuses a lot the grass installation which relies on the "system"-python
-  When conda/miniconda is not installed the installtion of grass is way smoother 
-  When installing conda, grass doesn't start anymore...

## Tried options
- install `fmask` and `rios` from source
- install them into different locations
- run the grass-script from within the directory where conda places it
- put the `~/miniconda3/bin` at the end and teh beginning of the `PATH`-variable
- add an alias for conda init in `.bashrc`
- 

## Solution
- Remove any `conda`-initialization from `.profile`, `.bash_profile` or `.bashrc`
- Remove/uncomment  especially any line like: `export PATH = "/home/usr/miniconda3/bin:$PATH"
- Create an alias in your `.profile` or `.bashrc` for actvatiing `conda`
	+  alias condainit='export PATH="/path/to/conda/bin:$PATH"'
	+ run `source .bashrc`
	+ "default" python sould be system python
- add `~/home/miniconda3/bin` to the path, e.g.

	+ `export PATH=/home/robin/.local/bin:/home/robin/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/robin/miniconda3/bin/`
- set proper "PROJ_LIB"-Environment-Variable (I did it in the python-script) 
	+`os.environ["PROJ_LIB"] = "/home/robin/miniconda3/share/proj"`

