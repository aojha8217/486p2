from porter2 import stem
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

################################################ PREPROCESSING CODE #####################################################################
wierdContractions = {"ain't":["am","not"], "amn't":["am","not"],"dasn't":["dare","not"], "e'er":["ever"],"shan't":["shall","not"],"won't":["will","not"],"y'all":["you","all"], "how's":["how","is"],"it's":["it","is"],"let's":["let","us"],"she's":["she","is"],"somebody's":["somebody","is"],"that's":["that","is"],"there's":["there","is"],"what's":["what","is"],"who's":["who","is"],"where's":["where","is"]}

def removeStopwords(inputArray):
	stopWords = open("stopwords").readlines()
	for x in stopWords:
		while x.strip() in inputArray:
			inputArray.remove(x.strip())
	return inputArray



def stemWords(inputArray):
	for x in range(len(inputArray)):
		#inputArray[x] = ps.stem(inputArray[x])
		inputArray[x] = stem(inputArray[x])
	return inputArray




def removeEdges(word):
	if word == "j." or word == "ae." or word == "scs." or word == "proc." or word == "jnl." or word == "phil." or word == "cam.":
		return word
	while word != "" and not (word[0].isalnum()):
		word = word[1:len(word)]
	counter = 1

	while word != ""  and not (word[len(word)-counter].isalnum()):
		if word[len(word)-counter] != '\'' or word[len(word)-counter] != '.':
			if(counter != 1):
				word =  word[:len(word)-counter] + word[len(word)-counter+1:]
			else:
				word = word[:len(word)-counter]
			#counter +=2
		else:
			counter +=1
		#print (word + ", "+ str(counter))
	return word


def removePeriods(word):
	if word == "j." or word == "ae." or word == "scs." or word == "proc." or word == "jnl." or word == "phil." or word == "cam.":
		return word
	if word == "." or word == "":
		return ""
	if word.find(".") == -1:
		return word
	elif word.find(".") == len(word)-1 and (word != "Dr." or word != "Mr." or word != "Mrs." or word != "St."):
		return word[:len(word)-1]
	return word


def removeApostrophe(word):
	if word.find("'") == -1:
		return [word]
	if word in wierdContractions:
		return wierdContractions[word]
	if "'t" in word:
		word = word.replace("n't","")
		return [word,"not"]
	if "'re" in word:
		word = word.replace("'re","")
		return [word,"are"]
	if "'d" in word:
		word = word.replace("'d","")
		return [word,"would"]
	if "'ll" in word:
		word = word.replace("'ll","")
		return [word,"will"]
	if "'ve" in word:
		word = word.replace("'ve","")
		return [word,"have"]
	if "'s" in word or "s'" in word:
		word = word.replace("'s","")
		return [word,"'s"]
	if"o'" in word or "l'" in word:
		return [word]
	else:
		word = word.replace("'"," ")
		return word.split()










def removeSGML(input):
    p = re.compile(r'<.*?>')
    return p.sub('', input)


def tokenizeText(input):
	input = removeSGML(input)
	finalWords = []
	allWords = input.split()
	for index in range(len(allWords)):
		allWords[index] = allWords[index].lower()
		allWords[index] = removeEdges(allWords[index])
		allWords[index] = removePeriods(allWords[index])
		#print(allWords[index] +" wtf")
		tempArray = removeApostrophe(allWords[index])
		#print(tempArray)
		for x in tempArray:
			if x != "":
				finalWords.append(x)



	
	#tokenData = tokenizeText(finalWords)
	stoppedData  = removeStopwords(finalWords)
	stemmedWords = stemWords(stoppedData)
	return stemmedWords

################################################ END PREPROCESSING CODE ################################################ 

def indexDoc(tokenText,index):	
	docID = tokenText[0]

	index['maxTf'].append(0)
	for x in tokenText:
		if docID not in index['DocProperties']:
			index['DocProperties'][docID] = []
		if x not in index['DocProperties'][docID]:
			index['DocProperties'][docID].append(x)

		if x not in index:
			index[x]  = {'Docs':{},}
		if docID not in index[x]['Docs']:
			index[x]['Docs'][docID] = 0
		index[x]['Docs'][docID] +=1
		if index[x]['Docs'][docID] > index['maxTf'][int(docID)-1]:
			index['maxTf'][int(docID)-1] = index[x]['Docs'][docID]
	return index



def indexQuery(tokenText,index):
	docID = 1
	index['maxTf'].append(0)
	for x in tokenText:
		#For later when calculating the inverted index
		if docID not in index['DocProperties']:
			index['DocProperties'][docID] = []
		if x not in index['DocProperties'][docID]:
			index['DocProperties'][docID].append(x)

		if x not in index:
			index[x]  = {'Docs':{},}
		if docID not in index[x]['Docs']:
			index[x]['Docs'][docID] = 0
		index[x]['Docs'][docID] +=1
		if index[x]['Docs'][docID] > index['maxTf'][int(docID)-1]:
			index['maxTf'][int(docID)-1] = index[x]['Docs'][docID]
	return index



def calcNormalizationQuery(index,docIndex,schemeQuery):
	for doc in index['DocProperties']:
		index['Norms'][doc] = 0.0
		for word in index['DocProperties'][doc]:
			if schemeQuery == "tfidf":
				if word in docIndex:
					#index['Norms'][doc] += math.sqrt(math.pow((float(index[word]['Docs'][doc])/float(index['maxTf'][int(doc)-1])),2) * math.pow(math.log10(float(docIndex['TotalDocs']) /float(len(docIndex[word]['Docs']))),2))
					index['Norms'][doc] += (math.pow((float(index[word]['Docs'][doc])/float(index['maxTf'][int(doc)-1])),2) * math.pow(math.log10(float(docIndex['TotalDocs']) /float(len(docIndex[word]['Docs']))),2))
				# else:
				# 	#index['Norms'][doc] += math.sqrt(math.pow((float(index[word]['Docs'][doc])/float(index['maxTf'][int(doc)-1])),2) * math.pow(math.log10(float(docIndex['TotalDocs']) / 1),2))
				# 	index['Norms'][doc] += (math.pow((float(index[word]['Docs'][doc])/float(index['maxTf'][int(doc)-1])),2) * math.pow(math.log10(float(docIndex['TotalDocs']) / 1),2))
			else:
				if word in docIndex:
					index['Norms'][doc] += (math.pow(math.log10((float(docIndex['TotalDocs']) - float(len(docIndex[word]['Docs']))) /float(len(docIndex[word]['Docs']))),2))
				# else:
				# 	index['Norms'][doc] += (math.pow(math.log10((float(docIndex['TotalDocs']) - 1.0) /1.0),2))

					

	return index

def calcNormalization(index,schemeDocs):
	for doc in index['DocProperties']:
		index['Norms'][doc] = 0.0
		for word in index['DocProperties'][doc]:
			if schemeDocs == "tfidf":#Summing weights squared using the tfidf weighting scheme 
				#index['Norms'][doc] += math.sqrt(math.pow((float(index[word]['Docs'][doc])/float(index['maxTf'][int(doc)-1])),2) * math.pow(math.log10(float(index['TotalDocs']) /float(len(index[word]['Docs']))),2))
				index['Norms'][doc] += (math.pow((float(index[word]['Docs'][doc])/float(index['maxTf'][int(doc)-1])),2) * math.pow(math.log10(float(index['TotalDocs']) /float(len(index[word]['Docs']))),2))
			else:
				#index['Norms'][doc] += math.sqrt(  math.pow((0.5 + ((.5*float(index[x]['Docs'][doc]))/float(index['maxTf'][int(doc)-1]))),2))
				index['Norms'][doc] += (math.pow((0.5 + ((.5*float(index[word]['Docs'][doc]))/float(index['maxTf'][int(doc)-1]))),2))


	return index

def indexDocument(docText,schemeDocs,schemeQuery,index):
	tokenText = tokenizeText(docText)
	index = indexDoc(tokenText,index)
	return index

def retrieveDocuments(query,index,schemeDocs,schemeQuery):
	tokenQuery = tokenizeText(query)
	queryIndex =  {'TotalDocs':1,'maxTf':[],'DocProperties':{},'Norms':{}}
	queryIndex = indexQuery(tokenQuery,queryIndex)
	queryIndex = calcNormalizationQuery(queryIndex,index,schemeQuery)
	finalList = {}
	counter = 0
	for x in queryIndex:
		if counter < 4:
			counter +=1
			continue

		#numDocsContaining = 1.0
		if x in index:
			numDocsContaining = float(len(index[x]['Docs']))
		else:
			continue

			
		if schemeQuery == "tfidf": #Query Weighting scheme for tfidf
			weightQuery = (float(queryIndex[x]['Docs'][1]) / float(queryIndex['maxTf'][0])) * math.log10(float(index['TotalDocs']) /numDocsContaining)
		else:#Query weighting scheme for nxx
			weightQuery = math.log10((float(index['TotalDocs']) - numDocsContaining) /numDocsContaining)

		if x in index:
			for doc in index[x]['Docs']:
				if schemeDocs == "tfidf":#Doc weighting scheme for tfidf
					currDocWeight = (float(index[x]['Docs'][doc]) /float(index['maxTf'][int(doc)-1])) * math.log10(float(index['TotalDocs']) /numDocsContaining)
				else:#Doc weighting scheme nxx
					currDocWeight = 0.5 + ((.5*float(index[x]['Docs'][doc]))/float(index['maxTf'][int(doc)-1]))
				if doc not in finalList:
					finalList[doc] = 0
				finalList[doc] += (currDocWeight*weightQuery)
	
	for y in finalList:
		#print(queryIndex['Norms'][1])
		finalList[y] /= (math.sqrt(queryIndex['Norms'][1])*math.sqrt(index['Norms'][y]))
	
	finalList = sorted(finalList.items(), key=operator.itemgetter(1), reverse = True)
	#print(finalList)
	return finalList





if __name__ == "__main__":
	schemeDocs = str(sys.argv[1])
	schemeQuery = str(sys.argv[2])
	folderDocs = str(sys.argv[3])
	folderQueries = str(sys.argv[4])

	if not (schemeDocs == "tfidf"  or schemeDocs == "nxx"):
		print("Invalid Document weighting Scheme")
		sys.exit()
	if not (schemeQuery == "tfidf"  or schemeQuery == "nxx"):
		print("Invalid query weighting Scheme")
		sys.exit()

	invertedIndex = {'TotalDocs':0,'maxTf':[],'DocProperties':{},'Norms':{}}
	for filename in glob.glob(os.path.join(folderDocs, "*")):
		invertedIndex['TotalDocs'] +=1
		inputFile = open(filename, 'r')
		data=inputFile.read().replace('\n', ' ')
		invertedIndex = indexDocument(data,schemeDocs,schemeQuery,invertedIndex)

	#print(invertedIndex['DocProperties'])	
	
	invertedIndex = calcNormalization(invertedIndex,schemeDocs)

	inputFile = open(folderQueries,'r')
	data =  inputFile.readlines()
	outputFilename = "cranfield."+str(schemeDocs)+"."+str(schemeQuery)+".output"
	f = open(outputFilename,"w+")
	counter = 1
	for line in data:
		final = retrieveDocuments(line,invertedIndex,schemeDocs,schemeQuery)
		for x in final:
			f.write(str(counter) +" "+ str(x[0]) + "\n")#+ " "+str(final[x]))
		counter +=1

	f.close()













