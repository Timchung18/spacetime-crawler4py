import sys
import re
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
import ast

url_list_file = open("url_list.txt", "r")
tknFrq_file = open("./Pages/tokenFreq.txt", "r")
page_wc_file = open("./Pages/pageWordCount.txt", "r")

report = open("report.txt", "w")

urlDict = dict()
line = url_list_file.readline()
while line:
    lsplit = line.split()
    if len(lsplit) != 2:
       pass
    else:
        urlDict[lsplit[0]] = lsplit[1]
    line = url_list_file.readline()


# 1. Unique Pages
# Total = len(URL_DICT)
page_count = len(urlDict)
report.write("1.\n" + "unique pages: " + page_count + "\n")

# 2. Longest Page
longest_page = ""
max_wc = 0
line = page_wc_file.readline()
while line:
    sLine = line.split(",")
    hash = sLine[0][:-4]
    count = sLine[1]
    if count > max_wc:
        max_wc = count
        longest_page = urlDict[hash]
    line = page_wc_file.readline()
report.write("\n2.\n" + "longest page: " + longest_page + "\n")


# 3. Find top 50 words
report.write("\n3.\n" + "50 most common words:\n")
line = tknFrq_file.readline()
lastLine = "{}"
while line:
    lastLine = line
    line = tknFrq_file.readline()
word_dict = ast.literal_eval(lastLine)
stop_wd_set = set(stopwords.words('english'))
freqOrder = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)

for word, freq in freqOrder:
    if word not in stop_wd_set:
        report.write(word + " : " + freq + "\n")


# 4. Per subdomain
# for each url: defaultdict[subdomain] += 1
# key = subdomain, value = count
# use regex to get subdomain from url
subDomPat = re.compile(r"^.*\/\/(.*)\.ics.uci.*")
subdomainDict = defaultdict(int)
for url in urlDict.values():
    match = re.match(subDomPat, url)
    if match:
        sd = match.group(1)
        subdomainDict[sd] += 1

report.write("\n4.\n" + "Number of Subdomains: " + len(subdomainDict) + "\n")
for sbdm, ct in sorted(subdomainDict.items()):
    report.write(sbdm + ", " + ct + "\n")

url_list_file.close()
tknFrq_file.close()
page_wc_file.close()

report.close()



