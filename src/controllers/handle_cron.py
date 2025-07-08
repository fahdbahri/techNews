import os
from services.list_sources import get_sources
from services.scrape_sources import scrape_sources
from services.generate_drafts import generate_drafts, convert_to_audio
from services.send_draft import send_drafts, send_audio
import json



async def handle_cron() -> None:
    try:
        print("Starting cron job...")
        cron_sources = await get_sources()
        raw_stories = await scrape_sources(cron_sources)
        raw_stories_string = json.dumps(raw_stories)
        draft_post = await generate_drafts(raw_stories_string)
        audio_file = await convert_to_audio(draft_post)
        result = await send_drafts(draft_post)

        if audio_file:
            audio_result = await send_audio(audio_file)
            print(f"Audio sent: {audio_result}")
        
            try:
                os.remove(audio_file)
                print(f"Audio file deleted: {audio_file}")
                
            except Exception as e:
                print(f"Error deleting audio file: {e}")


        print(result)        
    
    except Exception as e:
        print(f"Error in the function handle_crone: {e}")
