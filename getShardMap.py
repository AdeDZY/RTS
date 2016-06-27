#!/opt/python27/bin/python
import string
import sys, os
from os import listdir
from os.path import isfile, join, exists
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inferResDir", help="director containing inference results")
parser.add_argument("extidDir", help="director containing extid files")
parser.add_argument("shardNum",type = int, help="the file of externel IDs")
parser.add_argument("outputDir", help="output director")
args = parser.parse_args()

inferResDir = args.inferResDir
shardNum = args.shardNum 
outputDir = args.outputDir 

extid_file_paths = [f for f in listdir(args.extidDir) if isfile(join(args.extidDir, f)) and 'extid' in f]

shardMap = [list() for i in range(0, shardNum)]

for p in extid_file_paths:
	name = p.replace('.extid', '') 
	inferFilePath = inferResDir + '/' + name +  '.inference'
	if not exists(inferFilePath): continue
	print inferFilePath
	inferFile = open(inferFilePath, 'r')
	extidFile = open(args.extidDir + '/' + p)
	
	nLine = 0
	for line in inferFile:
		extid = extidFile.readline().strip()
		nLine += 1
		items = [int(item) for item in line.split(':')]
		intid = items[0] 
		shardID = items[1]

		# in case of missing docs
		while intid > nLine:
			nLine += 1
			extid = extidFile.readline().strip()
			print nLine, intid

		shardMap[shardID - 1].append(extid)
	
	inferFile.close()
	extidFile.close()

if not os.path.exists(outputDir):
	os.makedirs(outputDir)

for i in range(0, shardNum):
	outFile = open(outputDir+'/'+str(i + 1),'w')
	for extid in shardMap[i]:
		outFile.write(extid + '\n')

extidFile.close()
outFile.close()


