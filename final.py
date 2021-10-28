import sys
import re

# Find top 50 words

# Longest Page
# Read the URL file and create dictionary raw_URL -> hashed URL,  hashed -> raw
# Read tkCount, hashed URL -> word count, so then use hased URL to go raw_URL->word count
# Find max, use key to then find raw

# Unique Pages
# Total = len(URL_DICT)
# Per subdomain
# for each url: defaultdict[subdomain] += 1
# key = subdomain, value = count
# use regex to get subdomain from url
subDomPat = re.compile(r"^.*\/\/(.*)\.ics.uci.*")



