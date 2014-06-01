from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
from event import Event
import re
from datetime import datetime
import itertools
import pickle
import json

regex_start = re.compile('start date:(.*(?:am|pm))', flags=re.I)
regex_end = re.compile('end date:(.*(?:am|pm))', flags=re.I)
date_format = '%b %d, %Y %I:%M %p'
regex_loc = re.compile('maps\\.google\\.com/maps\\?q=(.*?)\\&amp;', flags=re.I)

def geocode(location):
    data = json.loads(urlopen('http://maps.googleapis.com/maps/api/geocode/json?%s' % urllib.parse.urlencode(dict(address=location))).read().decode())
    return data['results'][0]['geometry']['location']

def make_event_from_page(link):
    event = Event()
    event.link = link
    try:
        f = urlopen(link)
        soup = BeautifulSoup(f)
        main = soup.select(".sectionMain")[0]

        event.name = main.select(".subHeading")[0].get_text().strip()

        info = main.select(".secondaryContent")[0].get_text()

        sstart = regex_start.search(info).group(1).strip()
        event.start = datetime.strptime(sstart, date_format)

        send = regex_end.search(info).group(1).strip()
        event.end = datetime.strptime(send, date_format)

        event.location = urllib.parse.unquote_plus(regex_loc.search(str(main)).group(1).strip())
        event.coords = geocode(event.location)
    except Exception:
        pass

    return event

def get_links(src):
    print("Fetch links for %s" % src)
    f = urlopen(src)
    soup = BeautifulSoup(f)
    prefix = 'http://smashboards.com/'
    return [prefix + a['href'] for a in soup.select(".discussionList .listBlock.main a.PreviewTooltip")]

links = itertools.chain(*[get_links('http://smashboards.com/forums/tournament-listings.51/page-%d' % i) for i in range(1,2)])
events = []
for link in links:
    event = make_event_from_page(link)
    print(event)
    events.append(event)
    print("-------------------------")

with open('eventobjs.dat', 'wb') as f:
    pickle.dump(events, f)
