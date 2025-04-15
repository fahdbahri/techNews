from controllers.handle_cron import *
from dotenv import load_dotenv
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

load_dotenv()

async def main():
    # Create an async scheduler
    scheduler = AsyncIOScheduler()
    
    # Schedule the job
    scheduler.add_job(handle_cron, 'cron', hour='8', minute='30')
    
    try:
        scheduler.start()
        print("Scheduler started. Press Ctrl+C to exit")
        
        # Keep the script running
        while True:
            await asyncio.sleep(60)
            
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error in scheduler: {e}")




# async def main():
#     await handle_cron()

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except Exception as e:
#         print(f"Error in function main: {e}")