import pandas as pd
from transformers import pipeline






# Iterate through each dataframe and summarize it using the greedy decoder
def summarize_content(df, summarizer):

    df['summary'] = df['Content'].apply(lambda x: summarizer(x, truncation=True, max_length=50, min_length=10, do_sample=False)[0]['summary_text'])
    df = df.drop(columns=['Body', 'Content'])
    print(df["summary"])

    df.to_csv("/home/fahd/Documents/ai-powered-newsletter/AI-Powered-Newsletter/ai-processing/summarized_content.csv", index=False)
    

def main():
    df = pd.read_csv("scrapped_content.csv")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    summarize_content(df, summarizer)

if __name__ == "__main__":
    main()