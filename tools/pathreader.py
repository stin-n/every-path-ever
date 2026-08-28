# hi i wrote this myself :)
# be warned the code might be ass i'm still a beginner
# -stin

import os
from argparse import ArgumentParser

def readPaths(pathToRead, keepExtensions, outputFile, companyName, productName, excludedFiletypes=None, excludedFolders=None, includedFiletypes=None):
    # check compatibility
    if not excludedFiletypes == [] and not includedFiletypes == []:
        print("error: --excludeFile and --includeFile cannot be used together")
        exit()

    # check for company and product name
    hasComp = companyName != None
    hasProd = productName != None
    hasCompProd = hasComp and hasProd

    if hasComp and not hasProd:
        print("error: --company must be used with --product")
        exit()
    elif hasProd and not hasComp:
        print("error: --product must be used with --company")
        exit()

    # clear output file's contents
    f = open(outputFile, "w")
    f.write("")
    
    # get path to all files in pathToRead
    for (root,dirs,files) in os.walk(pathToRead,topdown=True):
        # trim full path to just the files in the root folder & subdirectories
        pathLen = len(pathToRead)
        rootTrimmed1 = root[pathLen:]

        # remove first slash from path if there is one
        rootTrimmed2 = rootTrimmed1
        if rootTrimmed1 != "" and rootTrimmed1[0] == os.sep: rootTrimmed2 = rootTrimmed1[1:]
        
        # format with arrow
        rootArrow = " -> ".join(rootTrimmed2.split(os.sep))


		# write to output
        f = open(outputFile, "a", encoding='utf-8')
        with f:
            for i in files:
                iL = i.lower()

                # skip if excluded folder name
                skipFolder = False
                for ef in excludedFolders:
                    efL = ef.lower()
                    lowerRoot = rootTrimmed1.lower()
                    efind = lowerRoot.find(efL)
                    if efind != -1: 
                        skipFolder = True
                    
                if skipFolder: continue
                
                # skip if excluded filetype
                skipExt = False
                noSkip = False
                excludedSet = excludedFiletypes != []
                includedSet = includedFiletypes != []

                if excludedSet:
                    for e in excludedFiletypes:
                        eL = e.lower()
                        if iL.endswith(eL): skipExt = True

                # skip if not included filetype
                elif includedSet:
                    for ift in includedFiletypes:
                        iftL = ift.lower()
                        if iL.endswith(iftL):
                            noSkip = True
                if includedSet and not noSkip: skipExt = True

                if skipExt:
                    continue

                # split extension from file
                curFile, curFileExt = os.path.splitext(i)

                # add back extensions if the --keepExt argument is specified
                newFile = curFile + curFileExt if keepExtensions else curFile

                # add company and product names if specified
                compProd = ""
                endTab = ""
                if hasCompProd:
                    compProd=f"{companyName}\t{productName}\t"
                    endTab = "\t"

                # combine directory and file with a tab separator
                finalPath = f"{compProd}{rootArrow}\t{newFile}{endTab}\n"

                f.write(finalPath)

scriptDir = os.path.dirname(os.path.realpath(__file__))
defOutput = "paths-output.txt"

parser = ArgumentParser(description="outputs directory structure to a file, for the \"every path ever\" spreadsheet")
parser.add_argument("-d", "--dir", default=scriptDir,
                    help="directory to scan, default is script's directory")
parser.add_argument("-c", "--company", 
                    help="name of the company/manufacturer to insert at the start of each line (optional, must be used with --product)")
parser.add_argument("-p", "--product",
                    help="name of the product to insert after the company (optional, must be used with --company)")
parser.add_argument("-k", "--keepExt", action="store_true",
                    help="keep file extensions instead of removing them from output by default")
parser.add_argument("-o", "--output", default=defOutput,
                    help=f"output file to write paths to, default is {defOutput}")
parser.add_argument("-e", "--excludeFile", nargs="+", default=[],
                    help="filetypes to exclude from the output (must not be used with --includeFile)")
parser.add_argument("-f", "--excludeFolder", nargs="+", default=[],
                    help="folder names to exclude from the output")
parser.add_argument("-i", "--includeFile", nargs="+", default=[],
                    help="filetypes to include in the output (must not be used with --excludeFile)")
args = parser.parse_args()

readPaths(args.dir, args.keepExt, args.output, args.company, args.product, args.excludeFile, args.excludeFolder, args.includeFile)

print(f"successfully exported paths to: {args.output}")