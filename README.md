# 📚 **Logos: Your Ultimate Bible Study Assistant**

**Logos** is an AI-powered assistant designed to help users study the Bible by answering questions with responses grounded in scripture, enriched with contextual insights and teachings from **The Bible Project** YouTube channel. This tool leverages advanced retrieval and generation techniques to provide meaningful, Bible-based responses to any question you ask.

## 📝 **Problem Description**

📖 Understanding the Bible can often be challenging, especially when seeking clear answers to complex spiritual questions or interpreting scriptural context for everyday situations. Misinterpretation of verses and lack of contextual understanding can hinder spiritual growth and proper application of biblical teachings.

### 🎯 **Objective**

The objective of this project is to develop an AI-powered Bible study assistant, **Logos** ✨, that provides clear, scripturally-based answers to users' questions. **Logos** not only retrieves Bible verses but also offers contextual insights and practical applications 🙏. It serves as a reliable tool for anyone looking to deepen their understanding of the Bible while ensuring accurate interpretation and direct reference to scripture 📜.

---

## 📊 **Data Source**

The data used in this project consists of Bible verses from the **King James Version (KJV)** stored as a JSON file and YouTube transcripts from **The Bible Project** 🎥, an educational YouTube channel known for its engaging videos that explain Biblical stories and themes. The transcript data is stored in the `data/` folder for use in this project.

- 📚 **Number of records**: All Bible verses
- 🎥 **YouTube transcripts**: Videos from [The Bible Project](https://www.youtube.com/@bibleproject)

For more detailed information about how to get the video transcripts, including instructions on how to convert them to a JSON file, please refer to the `data/README.md` 📂.

## Key Features

- **Ask Questions**: Users can ask any Bible-related question, and **Logos** will provide scripturally supported answers.
- **Scripture-Based Answers**: Each response is based on Bible verses, ensuring biblical accuracy and integrity.
- **Contextual Insights**: **Logos** explains the deeper meaning behind passages, incorporating related video teachings from **The Bible Project**.
- **Telegram Bot**: Access **Logos** on-the-go via the **Telegram bot** for quick responses to Bible questions.

---

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

---

## Installation

### Requirements

- **Python 3.8+**
- **Streamlit** for the web interface.
- **OpenAI API Key** for generating answers using GPT-4.
- **YouTube Data API Key** for fetching video transcripts from **The Bible Project**.
- **Elasticsearch** for retrieving Bible verses and video data.

Here's the revised setup section for your README, focusing only on using `venv`:

---

## ✨ Setup

### Local Setup

**Clone the Repository:**

```bash
git clone https://github.com/your-username/logos-bible-assistant.git
cd logos-bible-assistant
```

**Set Up the Python Environment:**

1. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. **Install the Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### How to Obtain API Keys

- **OpenAI API Key**:

  1. Sign up at [OpenAI](https://beta.openai.com/signup/).
  2. Navigate to the API section and generate a new API key.
  3. Copy the API key and add it to your `.env` file.

- **YouTube Data API Key**:

  1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
  2. Create a new project and enable the **YouTube Data API v3**.
  3. Create credentials and generate an API key.
  4. Copy the API key and add it to your `.env` file.

### Running the App Locally

1. **Run the app**:

   ```bash
   streamlit run app.py
   ```

2. Open your browser at `http://localhost:8501` to start interacting with **Logos**.

---

## How to Use

### On Telegram

1. Open Telegram and search for **Logos Bible Bot**.
2. Start a conversation, ask any Bible-related question, and get an answer with relevant scripture and insights from **The Bible Project**.

### On the Web

1. Once the Streamlit app is running, enter your question in the text box.
2. **Logos** will retrieve relevant Bible verses and insights to answer your question.

---

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

---

## How It Works

**Logos** uses a **Retrieval-Augmented Generation (RAG)** approach to provide insightful answers to Bible questions. It works in the following steps:

1. **Retrieval**: When a user asks a question, **Logos** retrieves relevant Bible passages from an Elasticsearch database and relevant video transcripts from **The Bible Project**.
2. **Answer Generation**: Using the **OpenAI GPT-4** model, **Logos** generates a response that combines scripture and insights from the retrieved video transcripts.
3. **Contextual Explanation**: The answer includes explanations of the Bible passages and their application to real-life situations.

---

## Environment Variables

The following environment variables are required:

- `OPENAI_API_KEY`: Your OpenAI API key for generating answers using GPT-4.
- `YOUTUBE_API_KEY`: Your YouTube Data API key for fetching **The Bible Project** video metadata and transcripts.

---

## Prerequisites

- **OpenAI Account**: Sign up at [OpenAI](https://beta.openai.com/signup/) to get an API key.
- **Google Cloud Account**: Sign up at [Google Cloud](https://console.cloud.google.com/) and create a project to access the YouTube Data API.
- **Elasticsearch**: Required for efficient retrieval of Bible passages and video transcripts.

---

## Results

### Example Query

**Question**: _"What does the Bible say about forgiveness?"_

**Response**:

```
"Be kind and compassionate to one another, forgiving each other, just as in Christ God forgave you." - Ephesians 4:32

Forgiveness is a central theme in the Bible, often tied to the mercy that God shows His people. The Bible teaches that forgiving others is not just a recommendation but a command. This is also illustrated in [The Bible Project's video on forgiveness](https://www.youtube.com/watch?v=XYZ), which discusses the theological significance of mercy and redemption in the biblical narrative.
```

---

## API Integration

- **OpenAI GPT-4**: Used to generate answers based on retrieved Bible verses and video transcripts.
- **YouTube Data API**: Used to fetch video metadata and transcripts from [**The Bible Project**](https://www.youtube.com/c/jointhebibleproject).
- **Elasticsearch**: For indexing and retrieving Bible passages and video data efficiently.

---

## Contact Information

For any questions or issues, feel free to reach out:

- **Project Lead**: [Your Name](oluwatobiiyanuoluwa24@gmail.com)
- **GitHub**: [Your GitHub](https://github.com/Tobai24)
