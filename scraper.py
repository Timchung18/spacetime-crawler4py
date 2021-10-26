import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import datetime

PATTERN_OBJECT = re.compile(r".*\.ics\.uci\.edu\/.*|.*\.ics\.uci\.edu$|"
                            r".*\.cs\.uci\.edu\/.*|.*\.cs\.uci\.edu$|"
                            r".*\.informatics\.uci\.edu\/.*|.*\.informatics\.uci\.edu$|"
                            r".*\.stat\.uci\.edu\/.*|.*\.stat\.uci\.edu$|"
                            r".*today.uci.edu/department/information_computer_sciences\/.*")
FRAG_PATTERN = re.compile(r"#.*")

URL_SET = set()  # set of all (hashed) URLs we've been to
URL_LIST_FILE = open("url_list.txt", "rw")  # holds all (hashed) URLS that we've been to
    
LINE = URL_LIST_FILE.readline()
while LINE:
    URL_SET.add(LINE)
    LINE = URL_LIST_FILE.readline()


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation requred.

    if resp.status > 600:
        return list()
    elif resp.status >= 300 < 400:
        return list()
    print(url)
    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    
    URL_LIST_FILE.write(url)
    save_file = open(url+".txt","w")  # TODO: hash the url for the text file name
    save_file.write(soup.get_text())
    
    ret_list = []

    for i in soup.find_all('a', href=True):
        if not re.match(FRAG_PATTERN, i['href']) and len(i['href']) > 0:  # filter out the fragments
            if i['href'][0] == "/":
                if len(i['href']) > 1 and i['href'][1] == "/":
                    if is_valid(i['href']):
                        print("valid",2, "https:"+i['href'])
                        ret_list.append("https:"+i['href'])
                    #else:
                    #    print("invalid",2, "https:"+i['href'])
                else:
                    if is_valid(url+i['href']):
                        print("valid", 3, url + i['href'])
                        print(i['href'])
                        ret_list.append(url + i['href'])
                    # else:
                    #     print("invalid",3,url+i['href'])
            else:
                if is_valid(i['href']):
                    print("valid", 4, i['href'])
                    ret_list.append(i['href'])
                #else:
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