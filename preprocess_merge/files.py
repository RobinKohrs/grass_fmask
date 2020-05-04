import os
import subprocess


files = [x for x in os.listdir(".") if x.endswith(".SAFE") and "L2A" in x]
f = open("files.txt", "w+")

for i in files:
    f.write(i + "\n")

print("""There are {} Sentinel2 L2A Products \n which will be merged
according to their date and band""".format(len(files)))
print(" ")


