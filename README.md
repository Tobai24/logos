📖 **Logos: Your Ultimate Bible Study Companion**

Hey there! 👋 Welcome to **Logos**, your go-to AI-powered Bible study assistant. Whether you're diving into scripture for the first time or looking for deeper insights, Logos has your back. This tool brings together the power of AI and **The Bible Project** YouTube channel to give you rich, scripture-based responses to any question you have. It's all about helping you explore the Bible with context, meaning, and purpose. ✨

## 📝 **Problem Description**

📖 To really understand scripture and discover its deeper meanings, it's important to have the guidance of the Holy Spirit. Sometimes, we might misinterpret verses or overlook their context, and that can slow down our spiritual growth and make it tougher to apply biblical teachings in our daily lives.

### 🎯 **Objective**

The goal of this project is to build an AI-powered Bible study assistant, **Logos** ✨, that gives you clear, scripture-based answers to your questions. **Logos** doesn't just pull Bible verses—it also provides context and practical insights 🙏, making it a powerful tool for anyone who wants to dive deeper into the Bible and understand it better. You'll get accurate interpretations, grounded in the Word 📜.

## 🌟 **Key Features**

- **Answer Bible Questions**: **Logos** provides clear, scripture-based answers to any Bible-related inquiry 📖, complete with direct references to relevant verses for accuracy.

- **Contextual Explanation**: For each referenced verse, **Logos** offers deeper insights 🔍, explaining its significance within the broader biblical narrative, including theological, historical, and cultural context.

- **Real-Life Application**: **Logos** helps users apply biblical teachings to daily life 🌍, offering practical advice rooted in scripture for situations like forgiveness, patience, and overcoming fear.

- **Friendly Guidance**: If a direct answer isn't available, **Logos** suggests related Bible passages 📜 and provides friendly guidance to encourage further exploration.

- **Telegram Bot**: Access **Logos** via the **Telegram bot** for quick and insightful answers to Bible-related questions anytime, anywhere.

## 📊 **Data Source**

For this project, we’re working with two main data sources: Bible verses from the **King James Version (KJV)** in JSON format, and transcripts from **The Bible Project** 🎥, a YouTube channel that explains Biblical stories and themes in a fun, engaging way. You’ll find the transcript data stored in the `data/` folder, ready to be used.

- 📚 **Number of records**: Every Bible verse from the KJV
- 🎥 **YouTube transcripts**: From videos by [The Bible Project](https://www.youtube.com/@bibleproject)

If you need help getting the video transcripts or converting them into JSON format, check out the `data/README.md` 📂 for step-by-step instructions.

## 🛠️ **Technologies**

- **Python 3.12**: Core programming language for developing the application.
- **Docker & Docker Compose**: Used for containerization and easy deployment.
- **Minsearch**: For efficient text search during development and practice.
- **Elasticsearch**: Used for full-scale search and retrieval in the production environment.
- **Streamlit**: Acts as the user interface.
- **Grafana**: Used for monitoring, with **PostgreSQL** as the backend database.
- **OpenAI**: Integrated for advanced language model (LLM) capabilities.
- **Google Cloud Account**: To access the YouTube Data API to get the video transcript. (not necessary the the data folder already has all the video transcript)

## Table of Contents

- [Installation](#installation)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Environment Variables](#environment-variables)
- [Prerequisites](#prerequisites)
- [Results](#results)
- [API Integration](#api-integration)
- [Contact Information](#contact-information)

## Installation

## ✨ Setup

### Local Setup

**Clone the Repository:**

```bash
git clone https://github.com/Tobai24/logos.git
cd logos
```

**Set Up the Python Environment:**

1. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows, use: venv\Scripts\activate
   ```

2. **Install the Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## How to Obtain API Keys

- **OpenAI API Key**:

  1.  Sign up at [OpenAI](https://beta.openai.com/signup/).
  2.  Navigate to the API section and generate a new API key.
  3.  Copy the key for later use.

## Save the API Key to Make It Private

1. **Create a `.envrc` File:**  
   Create a `.envrc` file in your project directory.

2. **Insert Your API Key:**  
   Copy `export OPENAI_API_KEY='YOUR_KEY'` to your `.envrc` file and insert your copied API key there.

## Preparation

1. **Install `direnv`:**  
   If you're on Ubuntu, run:

   ```bash
   sudo apt install direnv
   ```

2. **Configure Your Shell:**  
   Add `direnv` to your shell configuration by running:

   ```bash
   direnv hook bash >> ~/.bashrc
   ```

3. **Load the API Key:**  
   Run `direnv allow` to load the key into your environment.

4. **Best Practices:**  
   For OpenAI, it's recommended to create a new project and use a separate API key for security.

## Running the App Locally

1. **Run the app**:

   ```bash
   streamlit run app.py
   ```

2. Open your browser at `http://localhost:8501` to start interacting with **Logos**.

## How to Use

### On Telegram

1. Open Telegram and search for **Logos Bible Bot**.
2. Start a conversation, ask any Bible-related question, and get an answer with relevant scripture and insights from **The Bible Project**.

### On the Web

1. Once the Streamlit app is running, enter your question in the text box.
2. **Logos** will retrieve relevant Bible verses and insights to answer your question.

## Project Structure

```
logos-bible-assistant/
│
├── app.py                 # Streamlit web app
├── core/
│   ├── retrieval.py        # Logic for retrieving Bible verses and video transcripts
│   └── processing.py       # Text processing and context generation
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (API keys)
└── README.md               # Project documentation
```

## Contact Information

For any questions or issues, feel free to reach out:

- **Project Lead**: [Tobi](oluwatobiiyanuoluwa24@gmail.com)
- **GitHub**: [GitHub](https://github.com/Tobai24)

## 🎉 Special Mentions

A huge thank you to [DataTalks.Club](https://datatalks.club) for offering their LLM course for free! 🌟 The insights and skills I gained from their course were crucial in developing this project. If you want to enhance your expertise in building RAG application, I highly recommend checking out their [course](https://github.com/DataTalksClub/llm-zoomcamp). It’s an invaluable resource for diving into building LLM applications! 📚✨
