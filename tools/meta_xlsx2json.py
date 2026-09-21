# hi i wrote this myself :)
# 
# this is a script to convert the product-metadata excel sheet
# in /metastuff to a json file in the _split directory
# which will eventually probably be used by the website
# to display metadata about each product n shit
# 
# be warned the code might be ass i'm still a beginner
# also this requires the openpyxl module
# -stin

import json
import openpyxl
import os

# setup json vars
rootCom = ""
prod = ""
company = ""
productNames = []
types = []
formats = []
versionNames = []
tsvPath = ""
releaseDates = []
notes = ""
contributors = []
todo = ""

# setup script vars
prevRootCom = ""
curJson = {}
finalJson = {}

# get script directory and set paths to the xlsx and json files
scriptDir = os.path.dirname(os.path.realpath(__file__))
xlsxFile = f"{scriptDir}/metastuff/product-metadata.xlsx"
jsonFile = f"../_split/product-metadata.json"

# clear json file's contents
f = open(jsonFile, mode="w")
f.write("")

# load the xlsx file
wb = openpyxl.load_workbook(xlsxFile)
sheet = wb.active

# convert all None values to "" so it works with split()
def checkValid(input):
	return "" if input is None else input

# iterate through rows in the xlsx file
for row in sheet.iter_rows(min_row=2, values_only=True):
	rootCom = checkValid(row[0])
	prod = checkValid(row[1])
	company = checkValid(row[2])
	productNames = checkValid(row[3]).split(";")
	types = checkValid(row[4]).split(";")
	formats = checkValid(row[5]).split(";")
	versionNames = checkValid(row[6]).split(";")
	tsvPath = checkValid(row[7])
	releaseDates = checkValid(row[8]).split(";")
	notes = checkValid(row[9])
	contributors = checkValid(row[10]).split(";")
	todo = checkValid(row[11])

	# set json for current row
	curJson = {
		rootCom: {
			prod: {
				"company": company,
				"product_names": productNames,
				"types": types,
				"formats": formats,
				"version_names": versionNames,
				"tsv_path": tsvPath,
				"release_dates": releaseDates,
				"notes": notes,
				"contributors": contributors,
				"todo": todo
			}
		}
	}

	# append current row's json to the final json
	# and check if the root company is the same as the
	# previous row in order to make a tree-like output
	# e.g.
	# company1:
	#   product1: (stuff)
	#   product2: (stuff)
	# company2:
	#   product1: (stuff)

	if rootCom != prevRootCom:
		finalJson |= curJson
	else:
		finalJson[rootCom] |= curJson[rootCom]

	prevRootCom = rootCom

# write to json file
with open(jsonFile, mode="a", encoding="utf-8") as outJson:
	json.dump(finalJson, outJson, indent=4)

print("converted successfully")