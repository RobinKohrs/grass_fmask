import os
import shutil

tiffs = [tif for tif in os.listdir(".") if tif.endswith(".tif")]

for i in tiffs:
    date = i[7:15]
    path = os.getcwd()
    path_final = os.path.join(path, date)
    os.makedirs(path_final, exist_ok = True)
    shutil.move(i,path_final)
    

