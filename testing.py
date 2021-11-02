from difHash import *
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse
import re

re.compile(r"swiki.ics*\.")
url1 = "https://swiki.ics.uci.edu/doku.php/announce:winter-2021?do=media&ns=announce"
url2 = "https://swiki.ics.uci.edu/doku.php/announce:winter-2021?do=edit&rev=1610386120"

f = urllib.request.urlopen(url1)
soup = BeautifulSoup(f, "html.parser")
soupString = "".join(soup.strings)

newHash = DifHash(soupString)

g = urllib.request.urlopen(url2)
soup2 = BeautifulSoup(g, "html.parser")
soupString2 = "".join(soup2.strings)

newHash2 = DifHash(soupString2)

print(newHash, newHash2)
print(simCheck(newHash,newHash2))
parse = urlparse(url1)
print(parse.hostname)
print(parse.query)
