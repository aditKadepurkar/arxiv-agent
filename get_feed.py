import time
import signal
import os
import schedule
import feedparser
import requests
import json
import pandas as pd

# Function to activate the signal every 10 seconds, this is only for testing purposes
def activate_signal_every_10_seconds():
    parent_pid = os.getppid()
    while True:
        time.sleep(10)
        os.kill(parent_pid, signal.SIGUSR1)

def fetch_data_from_arxiv():
    # every midnight EST, fetch the data from arxiv
    def job():
        print("Fetching data from arxiv...")

        # currently just getting the feed for computer science
        feed = feedparser.parse('https://rss.arxiv.org/rss/cs')

        df = pd.DataFrame(feed.entries)
        df.to_csv('arxiv_feed.csv')

        # Send signal to parent process
        parent_pid = os.getppid()
        os.kill(parent_pid, signal.SIGUSR1)

    # Schedule the job
    schedule.every().day.at("00:01").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    activate_signal_every_10_seconds()