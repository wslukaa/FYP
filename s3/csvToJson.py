import csv
import json

csvfile = open('hashtagResult.csv', 'r')
jsonfile = open('hashtagResult.json', 'w')

fieldnames = ("id","ht_name","ts_start","t1", "t2", "predict", "kr", "dt", "kn", "lp", "rf", "gp", "ls")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')