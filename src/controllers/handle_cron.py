from services.list_sources import get_sources
from services.scrape_sources import scrape_sources
from services.generate_drafts import generate_drafts
from services.send_draft import send_drafts
import json



async def handle_cron() -> None:
    try:
        cron_sources = await get_sources()
        raw_stories = await scrape_sources(cron_sources)
        raw_stories_string = json.dumps(raw_stories)
        draft_post = await generate_drafts(raw_stories_string)
        result = await send_drafts(draft_post)

        print(result)        
    
    except Exception as e:
        print(f"Error in the function handle_crone: {e}")