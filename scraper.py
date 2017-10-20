# coding=utf-8

import scraperwiki
import lxml.html
import sqlite3
import re

BASE_URL = 'http://www.legislaturamendoza.gov.ar/nomina-senadores-periodo-2014-2018/'

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

    timesareaRegex = re.search(u'Período ([0-9]*) - ([0-9]*) - (.*)<\/br>', description)
    memberData['start_date'] = timesareaRegex.group(1)
    memberData['end_date'] = timesareaRegex.group(2)
    memberData['area'] = timesareaRegex.group(3)

    partyRegex = re.search('^(.*)<\/br>', description)
    memberData['party'] = partyRegex.group(1)

    facebookRegex = re.search('Facebook: <a href="(.*)"', description)
    if facebookRegex:
        memberData['facebook'] = facebookRegex.group(1)

    twitterRegex = re.search('Twitter: <a href="(.*)" target=_new>(.*)<\/a>', description)
    if twitterRegex:
        memberData['twitter'] = twitterRegex.group(2)

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
