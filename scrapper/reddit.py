import praw
import os
from dotenv import load_dotenv
import pandas as pd 

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SERCRET")
client_agent = os.getenv("CLIENT_USER")

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=client_agent,
)

df = pd.DataFrame()


subreddits = ['ArtificialInteligence', 'MachineLearning', 'artificial', 'Automate', 'singularity']

titles = []
bodys = []
content = []

def reading_subreddits(value):

        value = reddit.subreddit(value)
        print(f"reddit {value}")
        print()
        for submission in value.new(limit=5):
                titles.append(submission.title)
                bodys.append(submission.selftext)
                content.append(submission.title + ". " + submission.selftext)
        
        df['Title'] = pd.Series(titles)
        df['Body'] = pd.Series(bodys)
        df['Content'] = pd.Series(content)

        # saving content
        df.to_csv("/home/fahd/Documents/ai-powered-newsletter/AI-Powered-Newsletter/scrapper/scrapped_content.csv", index=False)


def get_content_news(subreddits):

        for subreddit in subreddits:
             
                reading_subreddits(subreddit)



if __name__ == "__main__":
        get_content_news(subreddits)