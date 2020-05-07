#remove last line from a text line in python
fd=open("D:\Test\sentinel-timestamp_space.txt","r")
d=fd.read()
fd.close()
m=d.split("\n")
s="\n".join(m[:-1])
fd=open("D:\Test\sentinel-timestamp_input.txt","w+")
for i in range(len(s)):
    fd.write(s[i])
fd.close()
