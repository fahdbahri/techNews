import os
from dotenv import load_dotenv


async def get_sources():
    try:

        # Load the environment
        load_dotenv()

        print("fetching sources...")

        # Get the API keys
        firecrawl_key = bool(os.getenv("FIRECRAWL_API"))

        # Reddit api keys
        client_id = bool(os.getenv("CLIENT_ID"))
        client_user = bool(os.getenv("CLIENT_USER"))
        client_secret = bool(os.getenv("CLIENT_SECRET"))


        sources = []

        if firecrawl_key:
            news_sources = [
                'https://arxiv.org/list/cs.LG/recent',
                'https://www.reuters.com/technology/artificial-intelligence/',
                'https://currentai.news/'
            ]
            sources.extend(news_sources) 
        
        # Reddit API 
        if client_id and client_secret and client_user:
            reddit_sources = [
                "https://www.reddit.com/r/LocalLLaMA/",
                "https://www.reddit.com/r/singularity/",
                "https://www.reddit.com/r/ControlProblem/"
                "https://www.reddit.com/r/technews/",
            ]

            sources.extend(reddit_sources)


        
        return sources
    
    except Exception as e:
        print(f"An error occured: {e}")
        return []
