# 📁 **App Folder**

This folder contains all the necessary files to run the **Streamlit app** and launch a **Telegram bot** for the application. Note that the app has not yet been deployed for project submission.

## 🚀 Getting Started

### Prerequisites

- Ensure you have **Docker** installed on your device. If you don’t have Docker, you can download it from [here](https://www.docker.com/get-started).

### Launching the Application

1. **Start Docker:**
   Run the following command in your terminal to start the Docker containers:

   ```bash
   docker-compose up -d
   ```

2. **Run Database Indexing:**
   Next, run the `database.py` script. This script contains the code needed to index the data into a vector database for retrieval.

   ```bash
   python database.py
   ```

3. **Setting Up Telegram Bot:**
   To start the Telegram bot, follow these steps:

   - Go to Telegram and search for the **BotFather**.
   - Use the command `/newbot` to create a new bot and follow the instructions to get your bot token.
   - Save the token as an environment variable. You can do this by adding the following line to your `.envrc` file:
     ```bash
     export TELEGRAM_BOT_TOKEN='your_bot_token_here'
     ```
   - After setting the token, run the `telegram_bot.py` script to keep the bot running:
     ```bash
     python telegram_bot.py
     ```

4. **Running the Streamlit App:**
   The `app.py` file contains all the relevant code needed to run the Streamlit app. Before running the app, ensure you have saved your **OpenAI API key** as an environment variable:

   ```bash
   export OPENAI_API_KEY='your_openai_api_key_here'
   ```

   Now, run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

5. **Accessing the App:**
   After launching the app, open your web browser and go to the forwarded app link to access the running application.
