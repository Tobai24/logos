# 📑 **Overview**

The `data/` folder contains essential components that enable the **Logos** Bible study assistant to function optimally:

1. **`kjv.json`**: Contains the full text of the **King James Version** (KJV) Bible, organized by book, chapter, verse, and text.
2. **`video_data.json`**: Stores metadata and transcript chunks from **The Bible Project's** YouTube videos, dynamically generated using the `transcript.py` script.
3. **`transcript.py`**: A Python script that extracts metadata and transcript data from YouTube videos of **The Bible Project** and saves the results in the `video_data.json` file.

## 📊 **Dataset Overview**

This section describes the structure and content of the dataset that **Logos** uses to provide answers based on both the Bible and The Bible Project’s YouTube videos.

### **About the Dataset**

- **Source**: Bible text from the **KJV Bible** and video transcripts from **The Bible Project's YouTube channel**. Visit [The Bible Project on YouTube](https://www.youtube.com/@bibleproject).
- **Files**:
  - **KJV JSON**: Contains all Bible verses categorized by books and chapters.
  - **Video Data JSON**: Contains YouTube video metadata and transcripts, segmented into manageable text chunks.

### **Video Metadata Fields in `video_data.json`**:

- **`video_id`**: Unique identifier for the YouTube video.
- **`title`**: Title of the video.
- **`author`**: Author of the video (usually "The Bible Project").
- **`publish_date`**: The date the video was published.
- **`text`**: Transcript text split into chunks.
- **`start`**: Timestamp indicating where each transcript chunk starts in the video.
- **`duration`**: Duration of the chunk in seconds.

## 🛠️ **How to Generate the YouTube Data (`video_data.json`)**

The `transcript.py` script is used to fetch metadata and transcripts of all videos on **The Bible Project’s** YouTube channel. Follow the steps below to create the `video_data.json` file.

### 📋 **Requirements**

- A **Google Cloud** account with access to the **YouTube Data API v3**.
- An API key for **YouTube Data API v3**.
- A Python environment with the following libraries installed:
  - `pytube`
  - `youtube_transcript_api`
  - `nltk`
  - `google-api-python-client`

> **Note**: If you've already installed the dependencies using `requirements.txt` as described in the project’s startup guide, you can ignore the dependencies part below.

### ⚙️ **Steps to Run the Script Locally**

1. **Get a YouTube Data API Key**:

   To obtain your YouTube Data API key, follow these steps:

   - **Access the Google Cloud Console**:

     - Sign up at [Google Cloud](https://console.cloud.google.com/)
     - Go to the [Google Cloud Console](https://console.cloud.google.com/)

   - **Create or Select a Project**:

     - If you have an existing project, select it from the dropdown menu at the top.
     - To create a new project, click on the **Select a Project** dropdown and then **New Project**.
     - Enter a project name and select an organization if applicable. Click **Create**.

   - **Enable the YouTube Data API v3**:

     - In the left sidebar, navigate to **APIs & Services** > **Library**.
     - Search for **YouTube Data API v3** and click on it, then click the **Enable** button.

   - **Create Credentials**:

     - After enabling the API, click on **Create credentials** at the top of the page.
     - In the dropdown, select **API key**.

   - **Restrict Your API Key** (Optional but recommended):

     - Click on **Restrict key** after generating your API key.
     - Under **Application restrictions**, choose either **HTTP referrers (web sites)** or **IP addresses** based on your use case.
     - Under **API restrictions**, limit the key to the **YouTube Data API v3**.
     - Click **Save** after configuring the restrictions.

   - **Copy Your API Key**:

     - Copy the API key displayed in the dialog. This key will allow your application to access the YouTube Data API.

   - **Store the API Key Securely**:

     - Store the key in a secure location. Avoid sharing it publicly; it’s best practice to use environment variables for managing sensitive information.

   - **Set Up Environment Variables**:
     - Store the API key as an environment variable to ensure security:
       ```bash
       export YOUTUBE_API_KEY="your_youtube_api_key"
       ```

2. **Run the Script**:

   - After ensuring all dependencies are installed, run the script to generate the `video_data.json` file:
     ```bash
     python transcript.py
     ```

3. **Dependencies**:

   - Ensure the following dependencies are installed via `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

### 🧩 **Key Parts of the Script**

- **API Key Loading**: The script securely loads your **YouTube Data API v3** key from an environment variable.
- **Extracting Video URLs**: It retrieves all video URLs from **The Bible Project’s** YouTube channel using the `google-api-python-client`.
- **Fetching Video Metadata**: The script uses `pytube` to retrieve metadata such as video title, author, and publication date.
- **Transcripts and Chunking**: The `youtube_transcript_api` library fetches transcripts, which are then broken into chunks of up to 200 tokens for easier use in the application.
- **Saving to JSON**: Metadata and transcripts are stored in the `video_data.json` file, formatted for easy reference and retrieval by the **Logos** app.

### 🔑 **How to Extract the Video ID**

The video ID is automatically extracted from the YouTube video URL. For example, if the URL is `https://www.youtube.com/watch?v=dQw4w9WgXcQ`, the video ID is `dQw4w9WgXcQ`.

## 📜 **Usage of Data**

The generated `video_data.json` file is utilized by the **Logos** app to provide accurate Bible study responses. The Bible verses from `kjv.json` and the video data from **The Bible Project**'s YouTube channel are used together to answer questions with scriptural support.

Ensure that the `video_data.json` file is placed in the appropriate directory and that the environment variables for API keys are properly set.
