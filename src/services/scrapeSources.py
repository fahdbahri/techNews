from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from listSources import *


load_dotenv()

# Load Firecrawl app 
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API"))

# Load the bearer token and endpoint for X
bearer_token = os.getenv("X_API_BEARER")
endpoint_url = "https://api.x.com/2/tweets/search/recent"

def request_headers(bearer_token: str) -> dict:

    return {"Authorization": "Beare {}".format(bearer_token)}

headers = request_headers(bearer_token)



# Define the schema of ur expected json


# Scrape the sources 

def scrape_sources(sources):
    num_sources = sources.length
    print(f"Scraping {num_sources} sources...")


    # configuring the toggel behaviour
    use_x = True
    use_reddit = True
    use_other = True



