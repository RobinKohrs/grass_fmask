#remove empty spaces from a text in python
with open('D:\Test\sentinel-timestamp.txt', 'r', encoding='utf-8') as inFile,\
     open('D:\Test\sentinel-timestamp_space.txt', 'w', encoding='utf-8') as outFile:
    for line in inFile:
        if line.strip():
            outFile.write(line)
