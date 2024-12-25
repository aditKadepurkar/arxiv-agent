from typing import List, Dict, Set
import asyncio
import json
import logging
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
import tracemalloc
import re
tracemalloc.start()

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TwitterScienceMonitor:
    def __init__(self, research_accounts: Dict[str, List[str]], keywords: List[str]):
        self.research_accounts = research_accounts
        self.keywords = set(keywords)
        self.subscribed_users = set()
        self.user_interests = {}
        
    
    async def get_data(self, twitter_account: str):
        username = os.getenv('LOGIN_USER')
        password = os.getenv('LOGIN_PASSWORD')
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 1024},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            )
            
            page = await context.new_page()
            
            try:
                await page.goto('https://twitter.com/i/flow/login', wait_until='networkidle')
                await page.fill('input[autocomplete="username"]', username)
                await page.click('button[role="button"]:has-text("Next")')

                await page.fill('input[type="password"]', password)
                await page.click('button[role="button"]:has-text("Log in")')
                
                await page.wait_for_selector('div[data-testid="primaryColumn"]', state='visible', timeout=30000)
            
                await page.goto(f'https://twitter.com/{twitter_account}', wait_until='load', timeout=60000)
                await page.wait_for_selector('article[data-testid="tweet"]', state='visible', timeout=30000)
                
                tweets_data = []

                tweets = await page.query_selector_all('article[data-testid="tweet"]')
                for tweet in tweets:
                    tweet_data = {}
                    
                    # ID
                    tweet_link = await tweet.query_selector('a[href*="/status/"]')
                    if tweet_link:
                        href = await tweet_link.get_attribute('href')
                        tweet_data['tweet_id'] = href.split('/')[-1]

                    # author information
                    author_element = await tweet.query_selector('div[data-testid="User-Name"]')
                    if author_element:
                        author_handle = await author_element.query_selector('span')
                        tweet_data['author_handle'] = await author_handle.inner_text() if author_handle else None

                    # timestamp
                    time_element = await tweet.query_selector('time')
                    if time_element:
                        tweet_data['created_at'] = await time_element.get_attribute('datetime')

                    # text
                    text_element = await tweet.query_selector('div[data-testid="tweetText"]')
                    if text_element:
                        tweet_data['text'] = await text_element.inner_text()

                    # hashtags
                    tweet_data['hashtags'] = re.findall(r'#(\w+)', tweet_data.get('text', ''))
                    tweet_data['mentions'] = re.findall(r'@(\w+)', tweet_data.get('text', ''))

                    # URLs
                    urls = await tweet.query_selector_all('a[href^="https://t.co/"]')
                    tweet_data['urls'] = [await url.get_attribute('href') for url in urls]

                    # media
                    media_elements = await tweet.query_selector_all('img[src*="https://pbs.twimg.com/card_img/"]')
                    tweet_data['media'] = [await img.get_attribute('src') for img in media_elements]
                    tweet_data['media type'] = 'image' if media_elements else None

                    if not media_elements:
                        print('no image')
                        try:
                            await tweet.wait_for_selector('video', state='visible', timeout=10000)
                            media_element = await tweet.query_selector('video')
                            if media_element:
                                tweet_data['media'] = await media_element.get_attribute('poster')
                                tweet_data['media type'] = 'video'
                            else:
                                tweet_data['media'] = None
                                tweet_data['media type'] = None
                        except Exception as e:
                            print(f"Video element not found: {str(e)}")
                            tweet_data['media'] = None
                            tweet_data['media type'] = None
                                        
                    # stats
                    repost_button = await tweet.query_selector('button[aria-label*="Repost"]')
                    retweets_text = await repost_button.get_attribute('aria-label')
                    retweets_count = int(re.search(r'\d+', retweets_text).group())

                    like_button = await tweet.query_selector('button[aria-label*="Like"]')
                    likes_text = await like_button.get_attribute('aria-label')
                    likes_count = int(re.search(r'\d+', likes_text).group())

                    tweet_data['reposts'] = retweets_count
                    tweet_data['likes'] = likes_count

                    tweets_data.append(tweet_data)

                print(tweets_data)
            except Exception as e:
                logger.warning(f"Failed: {str(e)}")
                await page.reload()
            
            finally:
                await browser.close()
        return

        


    async def subscribe_user(self, user_id: str, interests: Dict[str, List[str]]) -> Set[str]:
        """
        Subscribe a user to relevant Twitter accounts based on their interests.
        """
        try:
            self.user_interests[user_id] = interests
            
            matching_accounts = self._match_interests_to_accounts(interests)
            account_ids = await self._get_twitter_user_ids(matching_accounts)
            
            self.subscribed_users.add(user_id)
                        
            return matching_accounts
            
        except Exception as e:
            logger.error(f"Error subscribing user {user_id}: {str(e)}")
            raise

    def _match_interests_to_accounts(self, interests: Dict[str, List[str]]) -> Set[str]:
        """Match user interests to Twitter accounts."""
        matching_accounts = set()
        
        for keyword in interests.get('keywords', []):
            keyword = keyword.lower()
            for account, topics in self.research_accounts.items():
                if any(keyword in topic.lower() for topic in topics):
                    matching_accounts.add(account)
        
        for publication in interests.get('publications', []):
            publication = publication.lower()
            for account in self.research_accounts:
                if publication in account.lower():
                    matching_accounts.add(account)
                    
        return matching_accounts

   

async def test_fetch_tweets():
    # Initialize monitor with mock data
    research_accounts = {"@nature": ["science", "nature"]}
    keywords = ["science", "nature"]
    monitor = TwitterScienceMonitor(research_accounts, keywords)

    # subscribed_accounts = await monitor.subscribe_user('test_user', user_interests)
    subscribed_accounts = {'@nature'}
    print(f"Subscribed accounts: {subscribed_accounts}")
    
    try:
       await monitor.get_data('nature')
    except Exception as e:
        logger.error(f"Error fetching tweets: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_fetch_tweets())
