from controllers.handle_cron import *
from dotenv import load_dotenv
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime

load_dotenv()

async def main():
     print(f"News of Today: {datetime.now().strftime('%Y-%m-%d')}") 
     # Create an async scheduler
     scheduler = AsyncIOScheduler()
     
     # Schedule the job
     scheduler.add_job(handle_cron, trigger=IntervalTrigger(hours=48), next_run_time=datetime.now())
     
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




#async def main():
#     await handle_cron()
#
#if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except Exception as e:
#         print(f"Error in function main: {e}")
