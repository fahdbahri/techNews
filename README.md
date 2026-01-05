# Tech News

## Keep up with trending topics about new technologies all in one place for free.


Tech News is a solution for developers who are struggling to keep up with new trends, it analyzes from popular platforms, then sends it to Telegram.


## Demo


https://github.com/user-attachments/assets/4402d21c-12b5-486a-a60d-26fdfa4d38c9


## How It Works

1. **Data Collection**:
      - Monitors selected posts on websites and Reddit 
      - Monitors websites of your choice using crawl4ai 
      - Runs on a scheduled tims of your choice using cron jobs
      - For any duplicated content and news, it will be handled using Redis TLL to avoid any articles or news that you already been seen
2. **AI analyze**
      - generated drafts from the collected resources through Together AI
      - identifies emerging trends, what important releases, and news
      - Analyze sentiment and relevance
3. **Notification System**
      - Provide context about the trend and its resource (link, post, etc)
4. **Test to speach**
      - Convert the generated draft to an audio file using ElevenLabs for users to listen to


## Prerequisites

- Python
- Docker
- Docker Compose
- Telegram account
- API keys for required services (see Environment Variables)

## Enviroment Variable 

creating `.env` file and configure the following variables

```bash
# Generate the client keys from (https://www.reddit.com/prefs/apps)
CLIENT_ID=""
CLIENT_SECRET=""
CLIENT__USER=""

# Create a bot on Telegram using (https://core.telegram.org/bots#botfather)
TELEGRAM_BOT_TOKEN= ""
TELEGRAM_CHAT_ID=""


# Together api key to generate a draft (https://docs.together.ai/docs/quickstart)
TOGETHER_API_KEY=""

# Gemini API key for cleaning scraped sources with crawl4ai (free version is used) (https://ai.google.dev/gemini-api/docs/api-key)
GEMINI_API_KEY=""

# ElevenLabs API key for test to speach feature (https://elevenlabs.io/app/developers/api-keys)
ELEVENLABS_API_KEY=""
```

#### Note: You can include your favorite resources in `src/services/list_sourcs.py` Example:

```bash

        sources = []

    
        news_sources = [
                'https://techcrunch.com/',
                'https://www.dailyrotation.com/',
                'https://currentai.news/'
        ]
        sources.extend(news_sources) 
        
        # Reddit API 
        if client_id and client_secret and client_user:
            reddit_sources = [
                "https://www.reddit.com/r/LocalLLaMA/",
                "https://www.reddit.com/r/singularity/",
                "https://www.reddit.com/r/ControlProblem/"
                "https://www.reddit.com/r/technews/",
            ]

            sources.extend(reddit_sources)

```

## Getting started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/fahdbahri/technews.git
   cd technews
   ```

2. **Install Dependencies**:
   Make sure you have Python installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python src/main.py
   ```

## Docker Deployment

To make deployment easier, the project includes Docker configurations.

1. **Start the docker installation**:
   ```bash
   docker-compose up --build -d
   ```

2. **Stop the application**:
   ```bash
   docker-compose down
   ```

## Project structure

```bash
.
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker image configuration
├── LICENSE                 # Project license
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── src/
│   ├── controllers/        # Application controllers
│   ├── services/           # Application services
│   ├── __init__.py         # Python package initialization
│   └── main.py             # Main application entry point

```
