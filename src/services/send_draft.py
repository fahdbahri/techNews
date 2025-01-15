import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_drafts(draft_post: str):
    try:
        # Verify token and chat_id are available
        if not TOKEN:
            raise ValueError("Telegram Bot Token not found in environment variables")
        if not CHAT_ID:
            raise ValueError("Telegram Chat ID not found in environment variables")

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": draft_post,
            "parse_mode": "HTML"  # Optional: enables HTML formatting
        }

        # Use aiohttp instead of requests for async operations
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                result = await response.json()
                
                if not response.ok:
                    print(f"Telegram API Error: Status {response.status}")
                    print(f"Response: {result}")
                    
                    if response.status == 404:
                        print("Bot token is likely invalid. Please check your TELEGRAM_BOT_TOKEN")
                    elif response.status == 400:
                        print("Chat ID might be invalid or bot doesn't have access to the chat")
                        
                return result

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
        return {"ok": False, "error": str(ve)}
    except Exception as e:
        print(f"Error sending draft to Telegram: {e}")
        return {"ok": False, "error": str(e)}
