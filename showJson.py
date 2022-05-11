import json

fname = "diaDetail2.json"
with open(fname, 'r') as rfp:
    diaDetail = json.load(rfp)
for key in diaDetail.keys():
    print (diaDetail[key])
