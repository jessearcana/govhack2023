import urllib.request
import csv

outdir = "files/"
#iterate through files.csv, one line at a time, downloading each file
with open('oralhistorieswithtranscript.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == "RECORD#":
            continue    
        url = row[11]
        filename = row[0]
        try:
            urllib.request.urlretrieve(url, outdir+filename + '.pdf')
        except:
            print(url)
            pass
