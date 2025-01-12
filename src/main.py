from controllers.handle_cron import *
from dotenv import load_dotenv
import asyncio


load_dotenv()

async def main():
    print("Start process to generate draft...")
    await handle_cron()


if __name__ == "__main__":
    asyncio.run(main())