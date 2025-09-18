import os
from dotenv import load_dotenv, find_dotenv
from pydantic import HttpUrl, BaseModel, ValidationError
from typing import List
from datetime import datetime
import json
from together import Together
from elevenlabs.client import ElevenLabs
from elevenlabs import save


load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


# Define the schema
class Story(BaseModel):
    story_or_tweets_link: HttpUrl
    description: str


class DraftPost(BaseModel):
    interesting_stories_or_tweets: List[Story]


async def generate_drafts(raw_stories: str):

    try:

        together = Together()

        print(f"Generating a post draft with raw stories ({len(raw_stories)})")

        current_date = datetime.now().strftime("%m/%d")

        draft_post = DraftPost(interesting_stories_or_tweets=[])
        chat_completion = together.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': """You are given a list of raw AI and LLM-related tweets sourced from X/Twitter.
                Only respond in valid JSON that matches the provided schema(no extra keys).
                """
            },
            {
                'role': 'user',
                'content': f"""Your task is to find interesting trends, launches, or interesting examples from the tweets or stories.
                For each tweet or story, provide a 'story_or_tweet_link' and a one-sentence 'description'.
                Return all relevant tweets or stories as separate objects.
                Aim to pick at least 10 tweets or stories unless there are fewer than 10 available. If there are less than 10 tweets or stories, return ALL of them. Here are the raw tweets or stories you can pick from:\n\n{raw_stories}\n\n
                """
            }
        ],
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        response_format={
            'type': 'json_object',
            'schema': draft_post.schema()
        }
    )

    # Access the response content
        raw_json = chat_completion.choices[0].message.content

        if not raw_json:
            print("No JSON output returned from Together")
            return "No output."

        print(raw_json)

        try:
            parsed_response = json.loads(raw_json)
        except json.JSONDecodeError:
            print("Failed to parse json.")
            return "Invailid JSON output."

        header = f"🚀 Latest news from AI and LLM for {current_date}\n\n"

        draft_post = header + "\n\n".join(

            f"• {tweet_or_story['description']}\n  {tweet_or_story['story_or_tweets_link']}"

            for tweet_or_story in parsed_response.get('interesting_stories_or_tweets', [])

        )
    except Exception as e:
        print(f"Error in the function generate_draft: {e}")

    return draft_post




async def convert_to_audio(draft_post: str):
    try:
        # Remove links and format text for audio
        # This removes URLs and makes it more suitable for speech
        lines = draft_post.split('\n')
        audio_text = []
        for line in lines:
            if line.strip() and not line.strip().startswith('https'):
                # Remove bullet points and clean up for audio
                clean_line = line.replace('•', '').strip()
                if clean_line:
                    audio_text.append(clean_line)
        
        text_for_audio = '\n'.join(audio_text)
        
        # Use the correct ElevenLabs API method
        audio = client.text_to_speech.convert(
            text=text_for_audio,
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Fixed typo in voice ID
            model_id="eleven_monolingual_v1"
        )
        
        file_output = f"draft_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp3"
        
        # Save the audio to file
        save(audio, file_output)
        
        print(f"Audio file saved to {file_output}")
        return file_output
        
    except Exception as e:
        print(f"Error in the function convert_to_audio: {e}")
        return None
