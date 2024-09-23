import streamlit as st
import re
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import nltk
from elasticsearch import Elasticsearch
import openai
from openai import OpenAI
import json
import os

# Download NLTK data
nltk.download('punkt', quiet=True)

# OpenAI API Key
openai.api_key = "your-openai-api-key"

# Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Function to extract video ID from YouTube URL
def extract_video_id(url):
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return video_id_match.group(1) if video_id_match else None

# Function to get video metadata using pytube
def get_video_metadata(video_url):
    yt = YouTube(video_url)
    metadata = {
        "title": yt.title,
        "description": yt.description,
        "publish_date": yt.publish_date.isoformat(),
        "author": yt.author
    }
    return metadata

# Function to get transcript using youtube-transcript-api
def get_video_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_texts = [entry['text'] for entry in transcript]
    return " ".join(transcript_texts)

# Function to get OpenAI embedding
def get_embedding(text):
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response['data'][0]['embedding']

# Function to index the transcript in Elasticsearch
def index_transcript(video_id, transcript, metadata):
    chunks = nltk.tokenize.sent_tokenize(transcript)
    
    for index, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        doc = {
            "video_id": video_id,
            "text": chunk,
            "title": metadata['title'],
            "description": metadata['description'],
            "publish_date": metadata['publish_date'],
            "author": metadata['author'],
            "embedding": embedding
        }
        es.index(index="video_transcripts", id=f"{video_id}_{index}", body=doc)

# Function to perform vector search in Elasticsearch
def search_transcript(query):
    query_embedding = get_embedding(query)
    
    # Perform vector search in Elasticsearch
    search_body = {
        "size": 3,
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_embedding,
                    "k": 3
                }
            }
        }
    }
    
    response = es.search(index="video_transcripts", body=search_body)
    hits = response['hits']['hits']
    
    return [hit['_source'] for hit in hits]

# Function to generate a response using OpenAI based on context and user question
client = OpenAI()
def generate_answer(context, question):
    prompt = f"The following is a transcript snippet from a YouTube video:\n\n{context}\n\nQuestion: {question}\nAnswer:"
    response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{"role": "user", "content": prompt}]
)
    return response.choices[0].message.content.strip()

# Streamlit UI
st.title("YouTube Video Chatbot")
video_url = st.text_input("Enter YouTube Video URL:")

if video_url:
    video_id = extract_video_id(video_url)
    
    if video_id:
        metadata = get_video_metadata(video_url)
        transcript = get_video_transcript(video_id)
        
        # Index the transcript for the first time
        if not es.exists(index="video_transcripts", id=f"{video_id}_0"):
            index_transcript(video_id, transcript, metadata)
            st.success("Video transcript indexed successfully.")
        
        st.header(metadata['title'])
        st.write(f"**Description:** {metadata['description']}")
        st.write(f"**Published on:** {metadata['publish_date']}")
        st.write(f"**Author:** {metadata['author']}")
        
        user_question = st.text_input("Ask a question about the video:")
        
        if user_question:
            search_results = search_transcript(user_question)
            context = "\n".join([result['text'] for result in search_results])
            response = generate_answer(context, user_question)
            st.write("**Response:**", response)
    else:
        st.error("Could not extract video ID from URL.")

