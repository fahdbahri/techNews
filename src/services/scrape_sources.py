from dotenv import load_dotenv
from firecrawl import FirecrawlApp
import asyncpraw
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import List, Dict
import urllib.parse
import os
import aiohttp
import asyncio

load_dotenv()

# Load Firecrawl app
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API"))

# Load the bearer token and endpoint for X 
bearer_token = os.getenv("X_API_BEARER") 
endpoint_url = "https://api.x.com/2/tweets/search/recent"


# Define the the objects to store it

# Defining what a single story
class Story(BaseModel):
    headline: str
    link: str
    data_posted: str



class Stories:
    stories: List[Story]



# Requesting data by connecting to the endpoint

async def request_headers(bearer_token: str) -> dict:

    return {"Authorization": f"Bearer {bearer_token}"}


async def connect_to_endpoint(endpoint_url: str, headers: dict, parameters: dict, max_retries: int = 3) -> Dict[str, any]:
    retry_count = 0

    async with aiohttp.ClientSession() as session:
        while retry_count < max_retries:
            try:
                async with session.get(endpoint_url, headers=headers, params=parameters) as response: 
                    if response.status == 200: 
                        return await response.json() 
                    if response.status >= 400 and response.status < 500: 
                        print(f"Client error: {response.status}")
                        return 
                    retry_count += 1 
                    if retry_count < max_retries: 
                        await asyncio.sleep(min(2 ** retry_count, 60)) 
            except Exception as e: 
                if retry_count >= max_retries - 1: 
                    raise Exception( f"Failed after {max_retries} attempts: {e}") 
                retry_count += 1 
        
        raise Exception("Max retries exceeded")
# Scrape the sources   


async def scrape_sources(sources):    
    try:

        num_sources = len(sources)
        print(f"Scraping {num_sources} sources...")

        combined_text = {'stories': []}

        # configuring the toggel behaviour
        use_x = True
        use_reddit = True
        use_scrape = True

        for source in sources:
            print(f"Source: {source}")
            if "x.com" in source and use_x:

                username = source.split("/")[-1]
                print(username)

                query_username = f"from:{username} has:media -is:retweet -is:reply"
                encoded_username = urllib.parse.quote(query_username)

                # Tweets from the last 24 hours
                start_time = (datetime.now() - timedelta(days=1)
                              ).isoformat() + 'Z'

                encoded_start_time = urllib.parse.quote(start_time)

                query_parameters = {
                    "query": encoded_username,
                    "max_results": 10,
                    "start_time": encoded_start_time
                }

                headers = await request_headers(bearer_token)
                response_json = await connect_to_endpoint(endpoint_url, headers, query_parameters)
                
                
                if response_json is None:
                    print("No data recieved for now, we will try again later")
                elif response_json.get('meta', {}).get('result.count', 0):
                    print(f"No tweets in found in the username {username}")
                elif isinstance(response_json.get('data'), list):
                    print(f"Tweets found from username {username}")

                    stories = [
                        {
                            "headline": tweet['text'],
                            "link": f"https://x.com/i/status/{tweet['id']}",
                            "date_posted": start_time

                        }
                        for tweet in response_json['data']
                    ]

                    combined_text['stories'].extend(stories)

                else:
                    print(f"Expected an tweets.data to be an arrray: {response_json.get('data')}")

            elif "reddit.com" in source and use_reddit:

                username = source.split('/')[-2]

                start_time = (datetime.now() - timedelta(days=1)).timestamp()

                reddit = asyncpraw.Reddit(user_agent=os.getenv("CLIENT_USER"), client_id=os.getenv("CLIENT_ID"),
                                     client_secret=os.getenv("CLIENT_SECRET"))
                
                try:
                    async with reddit:
                        subreddit = await reddit.subreddit(username)
                        stories = []

                        async for post in subreddit.hot(limit=5):
                            story = [
                                {
                                    "headline": post.title,
                                    "link": post.url,
                                    "date_posted": post.created
                                }]
                            stories.append(story)
                            

                        combined_text['stories'].extend(stories)

                except Exception as e:
                    print(f"Error fetching reddit data: {e}")


            else:
                if use_scrape:
                    try:

                        current_date = datetime.now()
                        formatted_date = current_date.strftime("%x")

                        prompt_from_firecrawl = f"""
                                Return only today's AI or LLM related story or post headlines and links in JSON format from the page content.
                                They must be posted today, {formatted_date}. The format should be:
                                {{
                                "stories": [
                                    {{
                                        "headline": "headline1",
                                        "link": "link1",
                                        "date_posted": "YYYY-MM-DD"
                                    }}
                                ]
                                }}
                                If there are no AI or LLM stories from today, return {{"stories": []}}.
                                The source link is {source}.
                                If a story link is not absolute, prepend {source} to make it absolute.
                                Return only pure JSON in the specified format (no extra text, no markdown, no ```).
                                """

                        scrape_result = app.scrape_url(source, {
                            'formats': ['extract'],
                            'extract': {
                                'prompt': prompt_from_firecrawl,
                                'schema': Story.model_json_schema(),
                            }
                        })


                        today_stories = scrape_result['extract']
                        print(today_stories)
                        combined_text['stories'].extend(today_stories)
                    except Exception as e:
                        print(f"Error while fetching news resources: {e}")

        raw_stories = combined_text['stories']
        return raw_stories

    except Exception as e:
        print(f"Error in the function scrape_sources: {e}")
