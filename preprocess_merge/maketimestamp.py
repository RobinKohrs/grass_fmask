import os

# get mapset
mapset = input("plase specify the name of the mapset: ")

# get maps
##########
cwd = os.getcwd()
# get dirs with data
dirs = [x for x in os.listdir(".") if len(x) == 8 and os.path.isdir(x)]
realpaths = [os.path.join(cwd, x) for x in dirs]
# select band 2 in each directory
band2 = open("band2.txt","w+")
for i in realpaths:
    files = [x for x in os.listdir(i)]
    for band in files:
        if "B02" in band:
            date = band.split("_")[1]
            year = date[0:4]
            month = date[4:6]
            day = date[6:8]
            band2.write(band[0:-4] + "@" + mapset + "|" + year + "-" + month + "-" + day+ "\n")
        

