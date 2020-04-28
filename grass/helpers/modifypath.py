import sys
import os
import glob


# get some coloured output
class style():
    RED = '\033[31m'
    WHITE = '\033[37m'
    RESET = '\033[0m'


 
def findconda():

    # get current path variable
    current_path = os.getenv("PATH")
    path_split = current_path.split(os.pathsep)
    
    # when minicodna or anaconda at the beginning remove it
    if "miniconda" in path_split[0] or "anaconda" in path_split[0]:
        print(style.RED + "Your conda binary is at the beginning of the path-variable \n"
              "This script will remove it temporarily in order for Grass-Gis to find the correct python ")
        print(style.RESET)
    else:
        print("no problem")


    if  options["conda"] == "m":
        conda = "miniconda?"
        miniconda_path = glob.glob(os.path.expanduser("~") + os.sep + conda)[0]
        print("Your Path to Minicdonda:")
        print(miniconda_path)
        print(" ")

        # get miniconda binary and add it to path
        miniconda_bin = os.path.join(miniconda_path, "bin" + os.sep) 
        #os.environ["PATH"] = os.getenv("PATH")+ os.pathsep + miniconda_bin
        print("your current PATH-Variable looks like:")
        print(os.environ["PATH"])
        print(" ")

        # remove all entries with miniconda and only write it to the end
        path_all_conda = [i for i in path_split if "conda" in i]
        print("All 'conda'-like entries in your Path")
        print(path_all_conda)
        print(" ")
        path_no_conda = [j for j in path_split if j not in path_all_conda]
        print("path_no_conda") 
        print(path_no_conda)
        print(" ")

        for c, i in enumerate(path_no_conda):
            if c == 0:
                os.environ["PATH"] = i
            else:
                os.environ["PATH"] += os.pathsep + i
        
        print("after removing all the conda-directories, your path looks like:")
        print(os.getenv("PATH"))
        


        # set proj
        proj = os.path.join(miniconda_path, "share", "proj")
        os.environ["PROJ_LIB"] = proj
        print(" ")
        print("your current path to the 'proj'-library looks like:")
        print(os.getenv("PROJ_LIB"))

    # if using anaconda    
    elif options["conda"] == "a":

        conda = "miniconda?"
        miniconda_path = glob.glob(os.path.expanduser("~") + os.sep + conda)[0]
        print("Your Path to Minicdonda:")
        print(miniconda_path)
        print(" ")

        # get miniconda binary and add it to path
        miniconda_bin = os.path.join(miniconda_path, "bin" + os.sep) 
        #os.environ["PATH"] = os.getenv("PATH")+ os.pathsep + miniconda_bin
        print("your current PATH-Variable looks like:")
        print(os.environ["PATH"])
        print(" ")

        # remove all entries with miniconda and only write it to the end
        path_all_conda = [i for i in path_split if "conda" in i]
        print("All 'conda'-like entries in your Path")
        print(path_all_conda)
        print(" ")
        path_no_conda = [j for j in path_split if j not in path_all_conda]
        print("path_no_conda") 
        print(path_no_conda)
        print(" ")

        for c, i in enumerate(path_no_conda):
            if c == 0:
                os.environ["PATH"] = i
            else:
                os.environ["PATH"] += os.pathsep + i
        
        print("after removing all the conda-directories, your path looks like:")
        print(os.getenv("PATH"))

    else:
        print("either use miniconda or anaconda")
    return None


if __name__ == "__main__":
    options = dict()
    options["conda"] = str(sys.argv[1])
    #print(options)
    findconda()

