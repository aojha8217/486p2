import csv
import json
import webbrowser
import collections
import unittest
import sys
import glob
import os
import re
import math
import operator




def calculatePrecRecall(inputDict,jDict):
	prec = 0
	recall = 0
	for x in inputDict:
		prec += (float(inputDict[x]['numRelv']) / float(inputDict[x]['totalDocs']) )
		recall += (float(inputDict[x]['numRelv']) / float(jDict[x]['totalRelv']))
	prec = prec/float(len(inputDict))
	recall = recall/float(len(inputDict))
	f = (prec*recall)/(prec+recall)
	return(prec,recall,f)


def calcJudge(data):
	finalDict = {}
	for y in data:
		x = y.split()
		if x[0] not in finalDict:
			finalDict[x[0]] = {'totalRelv':0,'relvDocs':[]}
		finalDict[x[0]]['totalRelv'] +=1
		finalDict[x[0]]['relvDocs'].append(x[1])
	return finalDict



def calculateRelv(data,jDict,capNum):
	finalDict = {}

	for y in data:
		x = y.split()
		if x[0] not in finalDict:
			finalDict[x[0]] = {'numRelv':0,'totalDocs':0}
		if finalDict[x[0]]['totalDocs'] == capNum:
			continue
		finalDict[x[0]]['totalDocs'] += 1
		if x[1] in jDict[x[0]]['relvDocs']:
			finalDict[x[0]]['numRelv'] +=1

	return finalDict








if __name__ == "__main__":
	judgeFile = open("cranfield.reljudge",'r')
	jData = judgeFile.readlines()
	jDict = calcJudge(jData)
	judgeFile.close()

	tfidfFile = open("cranfield.tfidf.tfidf.output",'r')
	dataTfidf = tfidfFile.readlines()
	tfidfFile.close()




	# nxxFile = open("cranfield.tfidf.tfidf.output",'r')
	# dataNxx = nxxFile.readlines()
	# nxxRelv = calculateRelv(dataNxx,jDict,10)
	# nxxFile.close()
for cap in [10,50,100,500]:
	tfidfRelv = calculateRelv(dataTfidf,jDict,cap)
	precTfidf,recallTfidf,fTfidf = calculatePrecRecall(tfidfRelv,jDict)
	print("Precision for top "+str(cap)+" Documents : "+str(precTfidf))
	print("Recall for top "+str(cap)+" Documents : "+str(recallTfidf))
	print("F-Value for top "+str(cap)+" Documents : "+str(fTfidf))
	print("\n")









