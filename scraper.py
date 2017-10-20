# coding=utf-8

import scraperwiki
import lxml.html
import sqlite3
import re

START_YEAR = '2014'
END_YEAR = '2018'

BASE_URL = 'http://www.legislaturamendoza.gov.ar/nomina-senadores-periodo-{}-{}/'.format(START_YEAR, END_YEAR)

# Read in a page
html = scraperwiki.scrape(BASE_URL)
#
# # Find something on the page using css selectors
root = lxml.html.fromstring(html)
members = root.cssselect('div[class=\'bf-item\']')

parsedMembers = []

for member in members:

    memberData = {}

    memberData['id'] = member.cssselect('a')[0].attrib['data-attachment-id']

    memberData['image'] = member.cssselect('a')[0].attrib['href']

    memberData['name'] = member.cssselect('a')[0].attrib['data-caption-title'].replace('Sen. ', '')

    description = member.cssselect('a')[0].attrib['data-caption-desc']

    partyRegex = re.search('^(.*)<\/br>', description)
    memberData['party'] = partyRegex.group(1)

    facebookRegex = re.search('Facebook: <a href="(.*)"', description)
    if facebookRegex:
        memberData['facebook'] = facebookRegex.group(1)

    twitterRegex = re.search('Twitter: <a href="(.*)" target=_new>(.*)<\/a>', description)
    if twitterRegex:
        memberData['twitter'] = twitterRegex.group(2)

#     Facebook: &lt;a href=&quot;https://www.facebook.com/gustavo.arenas.980967&quot; target=_new&gt;Gustavo Arenas&lt;/a&gt;&lt;/br&gt;
# Twitter: &lt;a href=&quot;https://twitter.com/ArenasGustavo&quot; target=_new&gt;@ArenasGustavo&lt;/a&gt;&lt;/br&gt;

    memberData['start_date'] = START_YEAR
    memberData['end_date'] = END_YEAR

    print memberData

    parsedMembers.append(memberData)

print 'Counted {} Members'.format(len(parsedMembers))

try:
    scraperwiki.sqlite.execute('DELETE FROM data')
except sqlite3.OperationalError:
    pass
scraperwiki.sqlite.save(
    unique_keys=['id'],
    data=parsedMembers)
