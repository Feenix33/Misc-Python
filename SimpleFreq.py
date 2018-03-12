"""
SimpleFreq.py - py3
Count the frequency of words passed in a text file
Reads line by line, does not concatenate the next word
Regex splitting to address multiple types of separators and multiple consecutive separators
Input parameters
-i filename     Input file w/ext
-o filename     Output filename
-g #            Group by 1, 2, 3 words at a time, 0 does all groupings

Problems:
. No error handling
. General group by n not solved
"""

from collections import Counter
from itertools import tee, zip_longest
import argparse
import csv
import re

def countFrequency(infile, outfile, group):
    cnt = Counter()
    regexBase = "[:; \.,\n]"
    regexPattern = regexBase + regexBase + "*"
    with open(infile,"r") as fin:
        for line in fin:
            #wordList = line.split()
            #wordList = re.split('\W+', line)
            #wordList = re.split("[:; \.,\n][:; \.,\n]*", line[:-1])
            wordList = re.split(regexPattern, line[:-1])
            wordList = [word.lower() for word in wordList]
            if (group == 0 or group == 1):
                for word in wordList: # single words
                    cnt[word] += 1
            if (group == 0 or group == 2):
                for pairWords in pairwise(wordList): # pairs of words, progressive
                    key = pairWords[0] + "_" + pairWords[1]
                    cnt[key] += 1
            if (group == 0 or group == 3):
                for tripleWords in triplewise(wordList): # pairs of words, progressive
                    key = tripleWords[0] + "_" + tripleWords[1] + "_" + tripleWords[2]
                    cnt[key] += 1

    with open(outfile,"w") as fout:
        for key, value in cnt.items():
            fout.write ("{},{}\n".format(key, value))

def pairwise(iterable):
    a,b = tee(iterable)
    next(b, None)
    return zip(a,b)

def triplewise(iterable):
    a,b,c = tee(iterable, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a,b,c)


def groupwise(n, iterable, fillvalue=None):
    args = [iter(iterable)]*n
    return zip_longest(*args, fillvalue=fillvalue)

#--------------------------
def writeCSV(fname, listData):
    with open(fname, "w") as f:
        cw = csv.writer(f)
        cw.writerows(listData)

def buildInputParser(parser):
    parser.add_argument("-i", "--infile", nargs='?', const=1, type=str, default='in.txt', 
            help="input file with search parameters")
    parser.add_argument("-o", "--outfile", nargs='?', const=1, type=str, default='out.csv', help="Output file name")
    parser.add_argument("-g", "--group", nargs=1, type=int, default=[0], help="Group by 1,2,3. Group 0 means do all 1, 2, 3")

def main():
    inParser = argparse.ArgumentParser()
    buildInputParser(inParser)
    args = inParser.parse_args()
    countFrequency(args.infile, args.outfile, args.group[0])
    

#--------------------------

if __name__ == '__main__':
    main()
