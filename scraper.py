import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import datetime
import ast
import sys
from simhash import Simhash
from utils import get_urlhash
import os
import shelve
import urllib
import pickle

SIMH = shelve.open("simh.shelve")


save = open(os.path.join(sys.path[0], "simhb.txt"), "rb")
SIMHASH_SET = set()
line = save.readline()

#while line:
#    SIMHASH_SET.add(pickle.load()
#    line = save.readline()

while True:
    try:
        SIMHASH_SET.add(pickle.load(save))
        
    except EOFError:
        break

# SIMHASH_SET = ast.literal_eval(lastLine)

save.close()

simhash = open(os.path.join(sys.path[0], "simhash.txt"), "a")

PATTERN_OBJECT = re.compile(r".*\.ics\.uci\.edu\/.*|.*\.ics\.uci\.edu$|"
                            r".*\.cs\.uci\.edu\/.*|.*\.cs\.uci\.edu$|"
                            r".*\.informatics\.uci\.edu\/.*|.*\.informatics\.uci\.edu$|"
                            r".*\.stat\.uci\.edu\/.*|.*\.stat\.uci\.edu$|"
                            r".*today.uci.edu/department/information_computer_sciences\/.*")
FRAG_PATTERN = re.compile(r"#.*")

URL_SET = set()  # set of all (hashed) URLs we've been to
URL_LIST_FILE = open("url_list.txt", "r")  # holds all (hashed) URLS that we've been to

LINE = URL_LIST_FILE.readline()
while LINE:
    URL_SET.add(LINE)
    LINE = URL_LIST_FILE.readline()
URL_LIST_FILE.close()
URL_LIST_FILE = open("url_list.txt", "a")

SIMILARITY_THRESHOLD = .80

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # TODO: check if URL is in URL_SET, hash URL , then add url to URL_SET and to URL_LIST_FILE


    # TODO Look into what frontier.save is, if it saves all URLS and prevents cycles then don't need a lot of this support
    #   cant say that it does thouhg, not sure how it works exctly since it's a shelve file, shelf -> persistent dictionary


    if resp.status > 600:
        return list()
    elif resp.status >= 300 < 400:
        return list()
    print(url)
    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

    soupString = "".join(soup.strings)
    
    newHash = Simhash(soupString)

    # TODO probably change this to use SimhashIndex, apparently allows near duplicate querying in efficient way
    for v in SIMH.values():
        if newHash.distance(v) < SIMILARITY_THRESHOLD:
            return list()

    # TODO Double check this line
    #simhash.write(str(newHash)+'\n')

    #simhash.flush()
    #pickle.dump(newHash,simhash)
    #print(newHash.value)

    urlHash = get_urlhash(url)
    URL_LIST_FILE.write(urlHash + "," + url + "\n")
    save_file = open(os.path.join("./Pages", urlHash+".txt"), "w")  # TODO: hash the url for the text file name
    #save_file.write(soup.get_text())
    save_file.write(soupString)

    SIMH[urlHash] = newHash

    ret_list = []

    for i in soup.find_all('a', href=True):
        if not re.match(FRAG_PATTERN, i['href']) and len(i['href']) > 0:  # filter out the fragments
            if i['href'][0] == "/":
                if len(i['href']) > 1 and i['href'][1] == "/":
                    if is_valid(i['href']):
                        abs_path = urllib.parse.urljoin(url, i['href'])
                        print("valid",2, abs_path)
                        # ret_list.append("https:"+i['href'])
                        
                        if get_urlhash(abs_path) not in URL_SET:
                            ret_list.append(abs_path)
                        
                    #else:
                    #    print("invalid",2, "https:"+i['href'])
                else:
                    if is_valid(url+i['href']):
                        abs_path = urllib.parse.urljoin(url, i['href'])
                        print("valid", 3, abs_path)
                        print(i['href'])
                        # ret_list.append(url + i['href'])
                        
                        if get_urlhash(abs_path) not in URL_SET:
                            ret_list.append(abs_path)
                    # else:
                    #     print("invalid",3,url+i['href'])
            else:
                if is_valid(i['href']):
                    abs_path = urllib.parse.urljoin(url, i['href'])
                    print("valid", 4, abs_path)
                    # ret_list.append(i['href'])
                    if get_urlhash(abs_path) not in URL_SET:
                        ret_list.append(abs_path)
                #else:s
                #    print("invalid", 4, i['href'])

    return ret_list

def is_valid(url):
    try:
        parsed = urlparse(url)
        #if parsed.scheme not in set(["http", "https"]):
        #    return False

        if not re.match(PATTERN_OBJECT, parsed.geturl()):
            return False
        #  "*.ics.uci.edu/*", "*.cs.uci.edu/*", "*.informatics.uci.edu/*",
        #  "*.stat.uci.edu/*", "today.uci.edu/department/information_computer_sciences/*"

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv|php"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
