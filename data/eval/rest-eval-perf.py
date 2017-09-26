#!/usr/bin/python
#
# Script that sends questions from JSON file to the YodaQA web frontend
# REST API and prints results for error evaluation+analysis.
#
# Argument 1: JSON filename
# Argument 2: YodaQA URL (either "http://localhost:4567" or "http://qa.ailao.eu:4000")

import requests
import json
import sys
import time

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

argv = sys.argv
filename = argv[1]
URL = argv[2]
json_data = open(filename)
parsed_data = byteify(json.load(json_data))
number_of_questions = len(parsed_data)
question_counter = 0
correctly_answered = 0
recall = 0
finished = False
start = 0
finish = 0
timeT = 0
ansKG = 0
ansWiki = 0
agrLatKG = 0
agrLatWiki = 0

print('%-10.10s\t%.50s\t%.10s\t%.15s\t%.15s\t%.50s\t%s\t%s\t%s\t%s' % ("ID", "Question Text".ljust(50), "indicator", "correct answer".ljust(15), "found".ljust(15), "URL".ljust(50), "time", "Sniplets", "Sources", "SourceTypes"))

while question_counter < number_of_questions:
    questionText = parsed_data[question_counter]["qText"]
    try:
        questionAnswer = parsed_data[question_counter]["answers"][0]
    except IndexError:
        questionAnswer = ''
    ID = parsed_data[question_counter]["qId"]
    finished = False
    indicator = "incorrect"
    r = requests.post(URL+"/q", data={'text':questionText} )
    start = time.time()
    current_qID = byteify(r.json()["id"])
    while (finished == False): #wait for web interface to finish
        time.sleep(0.5)
        data = requests.get(URL +"/q/"+ current_qID).json()
        finished = data["finished"]
    
    finish = time.time()
    answer_list = byteify(data["answers"])
    sniplets = []
    sources = []
    srcType = set()
    for i in range (0, len(answer_list)): #iterate through answers and look for our correct one
        if (questionAnswer == answer_list[i]['text']): 
            if (i == 0):
                correctly_answered += 1
                indicator = "correct  "
		sniplets = answer_list[i]['snippetIDs']
		#print(str(sniplets))
		for i in range (0, len(sniplets)):
			#print(sniplets[i])
			snips = byteify(data["snippets"])
			#print(str(snips[str(sniplets[i])]))
			sources.append(snips[str(sniplets[i])]['sourceID'])
		for i in range (0, len(sources)):
			src = byteify(data["sources"])
			srcType.add(src[str(sources[i])]['type'])
			#print(str(src))
		if ( ('freebase' in srcType) or ('dbpedia' in srcType) ):
			ansKG += 1
			agrLatKG += (finish - start)
		else:
			ansWiki += 1
			agrLatWiki += (finish - start)
                continue
            else:
                recall	 += 1
                indicator = "recall   "
                continue
    print('%.10s\t%.50s\t%.10s\t%.15s\t%.15s\t%.50s\t%s\t%s\t%s\t%s' % (ID, questionText.ljust(50),indicator, questionAnswer.ljust(15), answer_list[0]['text'].ljust(15), (URL+"/q/"+str(current_qID)).ljust(50), str(finish - start), str(sniplets), str(sources), str(srcType)))
    question_counter += 1
    timeT = timeT + (finish - start)

print("correctly answered: " + str(correctly_answered))
print("recall: " + str(recall))
incorrect = number_of_questions-(recall+correctly_answered)
print("incorrect: "+ str(incorrect))
print("average time: "+ str(timeT / number_of_questions))
print("Answer Breakdown:")
print("KG: " + str(ansKG) + '/' + str(correctly_answered) + '=' + str(ansKG / correctly_answered))
print("Average latency: " + str(agrLatKG / max(ansKG, 1)))
print("not KG: " + str(ansWiki) + '/' + str(correctly_answered) + '=' + str(ansWiki / correctly_answered))
print("Average latency: " + str(agrLatWiki / max(ansWiki, 1)))



