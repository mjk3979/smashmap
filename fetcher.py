from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
from event import Event
import re
from datetime import datetime

regex_start = re.compile('start date:(.*(?:am|pm))', flags=re.I)
regex_end = re.compile('end date:(.*(?:am|pm))', flags=re.I)
date_format = '%b %d, %Y %I:%M %p'
regex_loc = re.compile('maps\\.google\\.com/maps\\?q=(.*?)\\&amp;', flags=re.I)


def make_event_from_page(link):
    f = urlopen(link)
    soup = BeautifulSoup(f)
    event = Event()
    main = soup.select(".sectionMain")[0]
    event.link = link

    event.name = main.select(".subHeading")[0].get_text().strip()

    info = main.select(".secondaryContent")[0].get_text()

    sstart = regex_start.search(info).group(1).strip()
    event.start = datetime.strptime(sstart, date_format)

    send = regex_end.search(info).group(1).strip()
    event.end = datetime.strptime(send, date_format)

    event.location = urllib.parse.unquote_plus(regex_loc.search(str(main)).group(1).strip())
    

    return event

print(make_event_from_page('http://smashboards.com/threads/jun-15-2014-super-smash-sundays-east-coast-5-red-bank-new-jersey.356635/'))
def get_links(src):
    print("Fetch links for %s" % src)
    f = urlopen(src)
    soup = BeautifulSoup(f)
    prefix = 'http://smashboards.com/'
    return [prefix + a['href'] for a in soup.select(".listBlock.main a.PreviewTooltip")]
