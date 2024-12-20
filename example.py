"""
This file will just have an example of using the RSS feed from arxiv
and using it to get the latest papers.

"""

import feedparser
import requests
import json
import os
import time
import datetime
import pandas as pd

DOWNLOAD_PDFS = False

# subscribe to the arxiv feed https://rss.arxiv.org/rss/cs (this is the computer science feed)
feed = feedparser.parse('https://rss.arxiv.org/rss/cs')

# sanity check get the entries in the feed
# print(feed.entries) # works
print(feed.entries[0].keys()) # get the keys of the first entry
print(len(feed.entries))

# save the feed to a json file
with open('arxiv_feed.json', 'w') as f:
    json.dump(feed, f)

# also make a csv file
df = pd.DataFrame(feed.entries)
df.to_csv('arxiv_feed.csv')

print(df.head())

links = list(df['link'])
# replace the arxiv link with the pdf link
for i, link in enumerate(links):
    links[i] = link.replace('abs', 'pdf')
    links[i] = links[i] + '.pdf'

print(list(links))

# download the pdfs
if DOWNLOAD_PDFS:
    for i, link in enumerate(links):
        r = requests.get(link)
        title = df['title'][i]
        title = title.replace('/', '_').replace('\\', '_')  # sanitize the title for file name
        with open(f'data/{title}.pdf', 'wb') as f:
            f.write(r.content)
        print(f'{title} downloaded to data/{title}.pdf')

# print the most recent and oldest papers using the time published

# it seems that all the entries have the same published time
# so it seems that the feed is updated every 24 hours?
# yes the feed is updated every 24 hours: 
# "RSS 2.0 and ATOM news feed pages are available for all active 
# subject areas within arXiv. Feeds are updated daily at midnight 
# Eastern Standard Time." - https://arxiv.org/help/rss
# 
# make use of https://blog.arxiv.org/2024/01/31/attention-arxiv-users-re-implemented-rss/
# for details on limits etc, also subscribing to multiple feeds and checking status of feeds
print(df.keys())
print('Most recent paper')
print(df['title'][0])
print(df['published'][0])
print('Oldest paper')
print(df['title'][len(df)-1])
print(df['published'][len(df)-1])


# check for updates every 10 seconds and save the new papers to the json file
while True:
    feed = feedparser.parse('https://rss.arxiv.org/rss/cs')
    with open('arxiv_feed.json', 'r') as f:
        old_feed = json.load(f)
    if feed.entries != old_feed.entries:
        print('New papers found')
        with open('arxiv_feed.json', 'w') as f:
            json.dump(feed, f)
    time.sleep(10)






