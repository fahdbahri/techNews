from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from listSources import *
import requests
import json
import re
from datetime import datetime, timedelta
import random
import time
from pydantic import BaseModel
from typing import List

load_dotenv()

# Load Firecrawl app
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API"))

# Load the bearer token and endpoint for X
bearer_token = os.getenv("X_API_BEARER")
endpoint_url = "https://api.x.com/2/tweets/search/recent"


# Define the the objects to store it

class Story(BaseModel):
    header: str
    link: str
    data_posted: str


class Stories:
    stories: List[Story]

# Requesting data by connecting to the endpoint


def request_headers(bearer_token: str) -> dict:

    return {"Authorization": "Beare {}".format(bearer_token)}


def connect_to_endpoint(endpoint_url: str, headers: dict, parameters: dict) -> json:
    """
    Connects to the endpoint and requests data.
    Returns a json with Twitter data if a 200 status code is yielded.
    Programme stops if there is a problem with the request and sleeps
    if there is a temporary problem accessing the endpoint.
    """
    response = requests.request(
        "GET", url=endpoint_url, headers=headers, params=parameters
    )
    response_status_code = response.status_code
    if response_status_code != 200:
        if response_status_code >= 400 and response_status_code < 500:
            raise Exception(
                "Cannot get data, the program will stop!\nHTTP {}: {}".format(
                    response_status_code, response.text
                )
            )

        sleep_seconds = random.randint(5, 60)
        print(
            "Cannot get data, your program will sleep for {} seconds...\nHTTP {}: {}".format(
                sleep_seconds, response_status_code, response.text
            )
        )
        time.sleep(sleep_seconds)
        return connect_to_endpoint(endpoint_url, headers, parameters)
    return response.json()

# Scrape the sources


def scrape_sources(sources):
    num_sources = sources.length
    print(f"Scraping {num_sources} sources...")

    # configuring the toggel behaviour
    use_x = True
    use_reddit = True
    use_scrape = True

    for source in sources:
        if "x.com" in source:
            if use_x:
                username_match = re.search(r'x\.com/([^/]+)', source)

                if username_match:
                    username = username_match.group(1)
                    print(username)
                else:
                    print("No match found")

                # Tweets from the last 24 hours
                start_time = (datetime.now() - timedelta(days=1)).timestamp()

                query_parameters = {
                    "query": f'from:{username} has:media -is:retweet -is:reply',
                    "max_results": 10,
                    "start_time": start_time
                }

                headers = request_headers(bearer_token)

                response = connect_to_endpoint(
                    endpoint_url, headers, query_parameters)

                response_json = response.json()

                if not response_json.get('meta', {}).get('result.count', 0):
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
                else:
                    print(f"Expected an tweets.data to be an arrray: {response_json.get('data')}")

            else:
                pass
