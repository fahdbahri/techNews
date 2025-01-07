import os
from dotenv import load_dotenv


def get_sources():
    try:

        # Load the environment
        load_dotenv()

        print("fetching sources...")

        # Get the API keys
        firecrawl_key = bool(os.getenv("FIRECRAWL_API"))
        x_bearer_token = bool(os.getenv("X_API_BEARER"))

        # Reddit api keys
        client_id = bool(os.getenv("CLIENT_ID"))
        client_user = bool(os.getenv("CLIENT_USER"))
        client_secret = bool(os.getenv("CLIENT_SECRET"))


        sources = []

        if firecrawl_key:
            news_sources = [
                'https://www.firecrawl.dev/blog',
                'https://openai.com/news/',
                'https://www.anthropic.com/news',
                'https://news.ycombinator.com/',
                'https://www.reuters.com/technology/artificial-intelligence/',
                'https://simonwillison.net/',
                'https://buttondown.com/ainews/archive/',
                'https://www.technologyreview.com/',
                'https://techcrunch.com/'
            ]
            sources.extend(news_sources)


        if x_bearer_token:
            x_sources = [
                "https://x.com/skirano"
            ]
            sources.extend(x_sources)
        
        # Reddit API 
        if client_id and client_secret and client_user:
            reddit_sources = [
                "https://www.reddit.com/r/huggingface/",
                "https://www.reddit.com/r/OpenAI/",
                "https://www.reddit.com/r/LangChain/",
                "https://www.reddit.com/r/deeplearning/"
            ]

            sources.extend(reddit_sources)


        
        return sources
    
    except Exception as e:
        print(f"An error occured: {e}")
        return []

