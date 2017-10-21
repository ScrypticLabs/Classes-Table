# -*- coding: utf-8 -*-
# @Author: Abhi
# @Date:   2017-10-21 12:40:17
# @Last Modified by:   Abhi
# @Last Modified time: 2017-10-21 14:06:30

import json
from pprint import pprint

def readJSON(filename):
	with open(filename) as rawData:
		data = json.load(rawData)
	return data

def writeJSON(data, filename):				# data should be a dictionary
	with open(filename, "w") as outfile:
		json.dump(data, outfile)

def getReview(professor, courseID, reviewsData):
	courseID_A, courseID_B = courseID
	for review in reviewsData:
		if review["Course_ID"] == courseID_A or review["Course_ID"] == courseID_B:
			if review["Professor"] == professor:
				return review["Review"]
	return ""

def parseCourseID(courseID):				# courseID in courses2v.json differs in format from reviews.json -> this method returns two possible keys that should match both formats
	index = -1
	for i in range(len(courseID)):
		if courseID[i].isdigit():
			index = i
			break
	return ({"letterKey" : courseID[0:index-1], "numberKey": courseID[index:]},{"letterKey" : courseID[0:index], "numberKey" : courseID[index:]})

def parseJSON(reviewsData, coursesData):	# creates the classes table
	classes = []
	for course in coursesData:
		for prof in course["instructors"]:
			_class = {}
			_class["ID"] = course["courseInfo"]["course_identifier"]+"_"+prof["name"]			# ID is in format courseID_profname
			try:
				_class["textbooks"] = course["textbookInfo"]["data"]["books"]["data"]["textbooks"]
			except TypeError:
				_class["textbooks"] = []														# the textbook data needs to be revised (it is inconsistent)
			_class["Avg-A-Range"] = ""															# Default value - implement in future
			_class["(not MVP) Avg Rating"] = [0.0]												# Default value - implement in future

			courseID_A, courseID_B = parseCourseID(course["courseInfo"]["course_identifier"])
			_class["review"] = getReview(prof["name"], (courseID_A["letterKey"]+" "+courseID_A["numberKey"], courseID_B["letterKey"]+" "+courseID_B["numberKey"]), reviewsData)
			classes += [_class]
	# pprint(classes)																				# if you'd like to see the final JSON in console
	writeJSON(classes, "classes.json")

if __name__ == "__main__":
	parseJSON(readJSON("reviews.json"), readJSON("coursesv2.json"))		# creates "classes.json" in local directory