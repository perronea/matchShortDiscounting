#!/usr/bin/env python

import csv, glob, os

#Seperate files into types
A = []
B = []
C = []
other = []

os.chdir("ShortDiscounting")
for file in glob.glob("*.csv"):
    with open(file, 'r') as f:
        wordlist = [line.split()[0] for line in f]
        if (len(wordlist[0]) == 34):
            A.append(file)
        elif (len(wordlist[0]) == 91):
            B.append(file)
        elif (len(wordlist[0]) == 1):
            C.append(file)
        else:
            other.append(file)

#Create dictionaries of file names and their date
Adate = {}
for files in A:
    with open(files, 'rb') as f:
        datecol = [line.split(",")[1] for line in f]
        date = datecol[0].replace('-', '/')
        Adate[files] = date
Bdate= {}
for files in B:
    with open(files, 'rb') as f:
        datecol = [line.split(",")[0] for line in f]
        parsedStr = datecol[1].split("    ")[1]
        date = parsedStr.replace('-', '/')
        Bdate[files] = date

#Create reference dictionary
with open('eprime_dates_addtl_JP.csv', 'rb') as f:
    reader = csv.reader(f)
    IDs = {}
    next(reader)
    for row in reader:
        IDs.setdefault(row[0], []).append(row[3])
        IDs.setdefault(row[1], []).append(row[3])
        if row[2] == "":
            continue
        else:
            IDs.setdefault(row[2], []).append(row[3])
#Correct date formatting
for key, value in IDs.iteritems():
    for date in value:
        parsed = date.split("/")
        if (parsed[0][0] == " "):
            parsed[0] = parsed[0].replace(' ', '')
        if (len(parsed[0]) == 1):
            parsed[0] = "0" + parsed[0]
        if (len(parsed[1]) == 1):
            parsed[1] = "0" + parsed[1]
        date = "/".join(parsed)
        IDs[key] = date


#Check if matched
for key in IDs:
    for files in Adate:
        underscoredFiles = files.replace('_', '-')
        if key in underscoredFiles:
            if Adate[files] == IDs[key]:
                print (underscoredFiles, key, Adate[files], IDs[key])
    for files in Bdate:
        underscoredFiles = files.replace('_', '-')
        if key in underscoredFiles:
            if Bdate[files] == IDs[key]:
                print (files, key, Bdate[files], IDs[key])



