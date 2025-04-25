# introducing techNews

This project aggregates news from key sources worldwide, summarizes it, and delivers real-time updates directly to you via Telegram.

## Features

- **AI-Powered Summaries**: Uses [Llama](https://github.com/facebookresearch/llama) to generate concise, accurate summaries of trending news.
- **Real-Time Notifications**: Stay updated on new trends and launches with instant Telegram Bot alerts.
- **Efficient Workflow**: Save time and focus on what's important by cutting through the noise of multiple platforms.
- **Open Source**: Clone it, customize it, and make it your own!

## Technologies Used

- **Python**: The backbone of the system.
- **Llama**: AI model for powerful summarization and content processing.
- **Firecrawl**: Web crawling for collecting posts and updates from key sources.
- **Together AI**: Collaboration and AI infrastructure.
- **Telegram Bot**: Sends real-time notifications to your Telegram account.

## How It Works

1. **Aggregates News**: Gathers updates from industry leaders and key influencers across platforms.
2. **Summarizes**: Uses Llama to provide concise, easy-to-digest summaries.
3. **Notifies**: Sends Telegram notifications whenever new trends or launches are detected.

## Installation

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

3. **Set Up Telegram Bot**:
   - Create a bot on Telegram using [BotFather](https://core.telegram.org/bots#botfather).
   - Save the bot token and update the code in the project to include your token.

4. **Run the Application**:
   ```bash
   python src/main.py
   ```

## Docker Deployment

To make deployment easier, the project includes Docker configurations.

1. **Build the Docker Image**:
   ```bash
   docker-compose build
   ```

2. **Run the Application**:
   ```bash
   docker-compose up
   ```
   
## Acknowledgments

Thanks to:
- The creators of [Llama](https://github.com/facebookresearch/llama) for their groundbreaking AI model.
- The [Together AI](https://together.xyz/) platform for seamless integration.
- The open-source community for making this project possible.

