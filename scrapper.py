import praw
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SERCRET")
client_agent = os.getenv("CLIENT_USER")

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=client_agent,
)

subreddits = ['MachineLearning', 'MachineLearningJobs']

def reading_subreddits(value):

        value = reddit.subreddit(value)

        print(value.display_name)

        print(value.title)

        print(value.description)


for subreddit in subreddits:
        
        reading_subreddits(subreddit)