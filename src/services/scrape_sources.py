from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
import asyncpraw
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import List, Dict
import urllib.parse
import os
import aiohttp
import asyncio
from .utils_cache import is_content_processed, mark_content_processed
from hashlib import sha256
import json

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")


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
                    raise Exception(f"Failed after {max_retries} attempts: {e}")
                retry_count += 1

        raise Exception("Max retries exceeded")


# Scrape the sources
async def scrape_sources(sources):
    try:
        num_sources = len(sources)
        print(f"Scraping {num_sources} sources...")

        combined_text = {'stories': []}

        use_reddit = True
        use_crawl4ai = True

        for source in sources:
            print(f"Source: {source}")

            if "reddit.com" in source and use_reddit:
                print("Using Reddit")

                username = source.split('/')[-2]

                start_time = (datetime.now() - timedelta(days=1)).timestamp()

                reddit = asyncpraw.Reddit(user_agent=os.getenv("CLIENT_USER"), client_id=os.getenv("CLIENT_ID"),
                                          client_secret=os.getenv("CLIENT_SECRET"))

                try:
                    async with reddit:
                        subreddit = await reddit.subreddit(username)
                        stories = []
                        redis_key = f"reddit/{username}"
                        if await is_content_processed(redis_key):
                            print("Skipping already processed story")
                        elif not await is_content_processed(redis_key):
                            async for post in subreddit.hot(limit=5):
                                story = [
                                    {
                                        "headline": post.title,
                                        "link": post.url,
                                        "date_posted": post.created
                                    }]
                                stories.append(story)
                                combined_text['stories'].extend(stories)

                                await mark_content_processed(redis_key)

                except Exception as e:
                    print(f"Error fetching reddit data: {e}")

            else:
                if use_crawl4ai:
                    try:
                        current_date = datetime.now()
                        formatted_date = current_date.strftime("%x")

                        prompt_from_crawl4ai = f"""Return AI/ML stories from today ({formatted_date}) as JSON:  
                        {{  
                          "stories": [  
                                      {{  
                                        "headline": "headline",  
                                        "link": "absolute_url",  
                                        "date_posted": "{formatted_date}"  
                                        }}  
                                      ]  
                          }}  
                        Only today's stories. Make links absolute. Pure JSON only."""

                        llm_config = LLMConfig(provider="gemini/gemini-2.0-flash", api_token=gemini_key)

                        llm_strategy = LLMExtractionStrategy(
                            llm_config=llm_config,
                            schema=Story.model_json_schema(),
                            extraction_type="schema",
                            instruction=prompt_from_crawl4ai,
                            chunk_token_threshold=1000,
                            apply_chunking=True, overlap_rate=0.0,
                            input_format="markdown"
                        )

                        crawl_config = CrawlerRunConfig(
                            extraction_strategy=llm_strategy,
                            cache_mode=CacheMode.BYPASS
                        )

                        browser_config = BrowserConfig(headless=True)

                        async with AsyncWebCrawler(config=browser_config) as crawler:
                            result = await crawler.arun(url=source, config=crawl_config)

                            if result.success:
                                print(f"Successfully scraped {source}") 

                                today_stories = json.loads(result.extracted_content)

                                print(f"stories: {today_stories}")

                                # Fix: Handle the structure properly
                                if isinstance(today_stories, list):
                                    # Handle list of results from crawl4ai
                                    for result_item in today_stories:
                                        if isinstance(result_item, dict) and 'stories' in result_item and not result_item.get('error', False):
                                            stories_list = result_item['stories']
                                            for story in stories_list:
                                                if isinstance(story, dict) and 'link' in story:
                                                    hashed_link = sha256(story['link'].encode()).hexdigest()
                                                    redis_key = f"crawl4ai/{hashed_link}"

                                                    if await is_content_processed(redis_key):
                                                        print("Skipping already processed story")
                                                    elif not await is_content_processed(redis_key):
                                                        combined_text['stories'].append(story)
                                                        await mark_content_processed(redis_key)
                                elif isinstance(today_stories, dict) and 'stories' in today_stories:
                                    # Handle single result object
                                    stories_list = today_stories['stories']
                                    for story in stories_list:
                                        if isinstance(story, dict) and 'link' in story:
                                            hashed_link = sha256(story['link'].encode()).hexdigest()
                                            redis_key = f"crawl4ai/{hashed_link}"

                                            if await is_content_processed(redis_key):
                                                print("Skipping already processed story")
                                            elif not await is_content_processed(redis_key):
                                                combined_text['stories'].append(story)
                                                await mark_content_processed(redis_key)

                    except Exception as e:
                        print(f"Error while fetching news resources: {e}")

        raw_stories = combined_text['stories']
        return raw_stories

    except Exception as e:
        print(f"Error in the function scrape_sources: {e}")
