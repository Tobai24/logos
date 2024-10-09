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

with open('../evaluation/embedding.json', 'r') as f:
    embedding = json.load(f)

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
            "text": { "type": "text" },  # Both Bible verses and video transcripts share this
            "text_vector": {"type": "dense_vector", "dims": 768, "index": True, "similarity": "cosine"}
        }
    }
}

index_name = "vector_db"

# Create the index

es_client.indices.delete(index=index_name, ignore_unavailable=True)
es_client.indices.create(index=index_name, body=index_settings)

for doc in tqdm(embedding):
    es_client.index(index=index_name, document=doc)
