import streamlit as st
import json
import openai
import pandas as pd
from openai import OpenAI
from tqdm.auto import tqdm
from elasticsearch import Elasticsearch
import time

# Initialize Elasticsearch client
es_client = Elasticsearch("http://localhost:9200")

with open('/root/practice/logos/data/video_data.json', 'r') as f:
    video_json = json.load(f)

with open('/root/practice/logos/data/kjv.json', 'r') as f:
    bible_json = json.load(f)
    
bible = bible_json["verses"]

index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": { 
        "properties": {
            # Fields for Bible verses
            "book": { "type": "text" },  # Bible-specific field
            "book_name": { "type": "keyword" },  # Bible-specific field
            "chapter": { "type": "text" },  # Bible-specific field
            "verse": { "type": "text" },  # Bible-specific field
            
            # Fields for YouTube transcripts
            "video_id": { "type": "keyword" },  # Video-specific field
            "title": { "type": "text" },  # Video-specific field
            "publish_date": { "type": "date" },  # Video-specific field
            "author": { "type": "text" },  # Video-specific field

            # Common field for both types of documents
            "text": { "type": "text" }  # Both Bible verses and video transcripts share this
        }
    }
}

index_name = "final_db"

# Create the index
es_client.indices.create(index='final_db', ignore=400, body=index_settings)

documents = bible + video_json

for doc in tqdm(documents):
    # Ensure each document has the expected structure for indexing
    if 'book_name' in doc:  # It's a Bible verse
        # Prepare for indexing
        es_client.index(index=index_name, document=doc)
    elif 'video_id' in doc:  # It's a YouTube transcript
        # Prepare for indexing
        es_client.index(index=index_name, document=doc)
