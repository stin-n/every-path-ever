import os
import csv
import json
import re

# replace non-alphanumeric characters with underscore
def cleanText(text):
	lowerText = text.lower()
	cleaned = re.sub(r"[^a-zA-Z0-9]", "_", lowerText)
	return cleaned

# set root directory
rootDir = f"..{os.sep}_split"

path = ""
thinge = {}
destJson = {}
prevRootCom = ""

# read all tsv files
for (root,dirs,files) in os.walk(rootDir,topdown=True):
	# trim full path to just the files in the root folder & subdirectories
	pathLen = len(rootDir)
	path = root[pathLen:]

	# setup vars
	jsonFile = rootDir + os.sep + "product-metadata.json"
	skipFile = False
	tsvPath = ""
	companyName = ""
	productName = ""
	rootCom = ""
	prod = ""

	for i in files:
		tsvPath = root + os.sep + i
		tsvPathTrimmed = path + os.sep + i

		# skip non .tsv files
		if not tsvPath.endswith(".tsv"):
			print("skipping file")
			continue

		print(f"full path: {tsvPath}")

		# get company and product name from tsv file
		with open(tsvPath, encoding="utf-8") as fd:
			rd = csv.reader(fd, delimiter="\t")
			for row in rd:
				companyName = row[0]
				productName = row[1]

		#print(f"product_name: {productName}, tsv_path = {tsvPathTrimmed}")

		# clean names
		rootCom = cleanText(companyName)
		cleant = cleanText(tsvPathTrimmed)
		lent = len(cleant)
		prod = cleant[1:lent-4]

		#print(f"cleaned names: {rootCom} - {prod}")
		
		# set up json
		thinge = {
			rootCom: {
				prod: {
					"company": companyName,
					"product_names": [productName],
					"formats": ["FILL IN"],
					"version_names": [""],
					"tsv_path": tsvPathTrimmed,
					"release_dates": ["?"],
					"description": "FILL IN",
					"notes": "",
					"contributors": ["FILL IN"],
					"todo": ""
				}
			}
		}
		destJson[rootCom] = thinge[rootCom]
		destJson[rootCom] |= thinge[rootCom]
		print(json.dumps(destJson, indent=4))

#with open("product-metadata.json", mode="w", encoding="utf-8") as outJson:
#	json.dump(destJson, outJson, indent=4)