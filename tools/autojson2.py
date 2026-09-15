import os
import csv

# set root directory
rootDir = f"..{os.sep}_split"

outFile = "allcomprod.txt"

# clear output file's contents
f = open(outFile, "w")
f.write("")

for (root,dirs,files) in os.walk(rootDir,topdown=True):
	# trim full path to just the files in the root folder & subdirectories
	pathLen = len(rootDir)
	path = root[pathLen:]

	tsvPath = ""

	for i in files:
		tsvPath = root + os.sep + i
		tsvPathTrimmed = path + os.sep + i
		tsvPathTrimmed = tsvPathTrimmed.replace("\\", "/")

		# skip non .tsv files
		if not tsvPath.endswith(".tsv"):
			print("skipping file")
			continue

		# get company and product name from tsv file
		with open(tsvPath, encoding="utf-8") as fd:
			rd = csv.reader(fd, delimiter="\t")
			for row in rd:
				companyName = row[0]
				productName = row[1]
		print(tsvPathTrimmed)

		with open(outFile, mode="a", encoding="utf-8") as f:
			f.write(f"{companyName}\t{productName}\t\t{tsvPathTrimmed}\n")