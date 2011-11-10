__author__ = 'agbattes'

"""
   User: agbattes
   Date: 11/4/11
   Time: 10:02 PM
   
"""

import datetime
import time
from calendar import timegm
import simplejson as json
import httplib2
import pprint

today = datetime.date.today()
one_day = datetime.timedelta(days=1)
tomorrow = today + one_day
print today, tomorrow
ts = int(time.mktime(tomorrow.timetuple()))
print ts



last_date = datetime.datetime(2011,10,26,0,0)

foursquare_data = []
FOURSQUARE_TOKEN = ""

more_data = True
offset = 0
h = httplib2.Http(".cache")

while more_data:
    fs_url = "https://api.foursquare.com/v2/users/self/checkins?oauth_token=%s&v=20111104&offset=%s&limit=100"%(FOURSQUARE_TOKEN, offset)
    print fs_url
    resp, content = h.request(fs_url, "GET")
    more_data = False
#    print content[0:300]
    data = json.loads(content)

    for item in data['response']['checkins']['items']:
#        print
#        pprint.pprint(item)
        date = datetime.datetime.fromtimestamp(item['createdAt'])
        print date
        if date>last_date:
            foursquare_data.append(item)
        else:
            more_data = False
            break
    offset += 100

print "# fs items ", len(foursquare_data)

data_out = []
for item in reversed(foursquare_data):
    pprint.pprint(item)
    h = {'createdAt': item['createdAt'],
         'title': item.get('shout', ''),
         'location': item['venue']['location'],
         'place': item['venue']['name'],
         'category':item['venue']['categories'] and  item['venue']['categories'][0] or {}}
    data_out.append(h)
#    break

sout = """
ffdata = %s;
"""%json.dumps(data_out)
f = open("data.js", "w+").write(sout)
