#!/opt/python27/bin/python
import os, sys
import string
import time
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("samplingTrial")
parser.add_argument("numClusters")
parser.add_argument("iterCount")
parser.add_argument("clusteringTrial")
parser.add_argument("weights", nargs=5, help="title heding url inlink body", type=float)
parser.add_argument("seeds")
parser.add_argument("--ref_threshold", "-r", type=float, default=1.0)
parser.add_argument("--lamda", "-l", type=float, default=0.1)
args = parser.parse_args()
print args

baseDir = '/bos/tmp11/zhuyund/RTS/'

#corresponding to different sampling trials
datFile = baseDir+'/output/sampled/sample'+args.samplingTrial+'.dat'
outputDir = baseDir + '/output/Kmeans/samplingTrial' + args.samplingTrial + '/'

lamda = str(args.lamda)
minVocabSeed = '3'

trialDir = outputDir + args.numClusters + 'Clusters-'+args.iterCount+'Iters-'+args.clusteringTrial+'/'
centroidDir = trialDir+'centroids/'

print outputDir
if not os.path.exists(outputDir):
	print outputDir
	os.makedirs(outputDir)

if not os.path.exists(trialDir):
	print trialDir 
	os.makedirs(trialDir)

if not os.path.exists(centroidDir):
	print centroidDir
	os.makedirs(centroidDir)

param_file = open(trialDir+'/param', 'w')
for k, v in vars(args).items():
	param_file.write(k + ':' + str(v) + '\n')
param_file.close()


logFile = trialDir+'log'
cmd = "/bos/tmp11/zhuyund/partition/Clustering-field-int/kmeans.sh "+datFile+" "+args.numClusters+" "+lamda+" "+args.iterCount+" "+centroidDir+" "+minVocabSeed+" "
cmd += '1 1 '
	
field_types = ["field", "wholeToField", "wholeToWhole", "Euclidean"]
cmd += " " + args.seeds + " " + field_types[0] + " "
cmd += str(args.ref_threshold) + " "
cmd += " >& " + logFile
print cmd
#r = random.random() * 60
#time.sleep(int(r))
os.system(cmd)

