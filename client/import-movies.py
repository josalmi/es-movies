import urllib2
from BeautifulSoup import BeautifulSoup
import json
import requests

esUrl = "http://elasticsearch:9200"

def title(row):
    return row.contents[1].string.replace("T:", "").strip()

def id(row):
    return row.contents[0].string.strip()

def bad(row):
    return not row.contents or len(row.contents) < 10 or not row.contents[0].string or "td>" in row.contents[0].string or title(row) == "title"

def year(row):
    if not row.contents[2].string or not row.contents[2].string.isdigit():
      return ""
    return row.contents[2].string.replace("x", "0").replace("D:","").strip()

def director(row):
    if not row.contents[3].string:
      return ""

    return row.contents[3].string.replace("D:", "").strip()

def producers(row):
    if not row.contents[4].string:
        return ""
    return map(unicode.strip, row.contents[4].string.replace("P:","").replace("PN:", "").replace("PZ", "").replace("PU:", "").strip().split(","))

def studio(row):
    if not row.contents[5].string:
        return ""
    return row.contents[5].string.replace("S:", "").replace("SU:", "").replace("ST:","").strip()

def process(row):
    if not row.contents[6].string:
        return ""
    return row.contents[6].string.replace("prc", "").strip()

def category(row):
    if not row.contents[7].string:
        return ""
    return map(unicode.strip, row.contents[7].string.strip().split(","))

def awards(row):
    if not row.contents[8].string:
        return ""
    return map(unicode.strip, row.contents[8].string.replace("aw", "").strip().split(","))

def location(row):
    if not row.contents[9].string:
        return ""
    return row.contents[9].string.strip()

def rowToMovie(row):
    if bad(row):
        return None

    return {
        'id': id(row),
        'title': title(row),
        'year': year(row),
        'director': director(row),
        'producers': producers(row),
        'studio': studio(row),
        'process': process(row),
        'category': category(row),
        'awards': awards(row),
        'location': location(row)

    }

def movieToBulk(movie):
    index = {"index": {
        '_index': "movies",
        '_id': movie['id'],
        '_type': 'movie'
    }}
    return json.dumps(index) + "\n" + json.dumps(movie) + "\n"

def load(bulk):
  headers = { 'content-type': 'application/x-ndjson' }
  return requests.post(esUrl + "/_bulk", data=bulk, headers=headers)

page = urllib2.urlopen("https://archive.ics.uci.edu/ml/machine-learning-databases/movies-mld/data/main.html")
soup = BeautifulSoup(page)
accumulator = []

for row in soup.findAll('tr'):
    movie = rowToMovie(row)
    if movie:
        accumulator.append(movieToBulk(movie))
        if (len(accumulator) == 100):
            print(load(''.join(accumulator)).text)
            accumulator = []
print(load('\n'.join(accumulator)).text)

