import json
import openai
import pandas as pd
from openai import OpenAI
from tqdm.auto import tqdm

from elasticsearch import Elasticsearch
es_client = Elasticsearch("http://localhost:9200")

def elastic_search(query, index_name = "final_db"):
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "should": [  # Use 'should' to match either condition
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["text^4", "book_name", "chapter", "verse", "book"],
                            "type": "best_fields"
                        }
                    },
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["title", "text", "author"],  # Fields for video transcripts
                            "type": "best_fields"
                        }
                    }
                ]
            }
        }
    }

    # Execute the search query
    response = es_client.search(index=index_name, body=search_query)

    result_docs = []
    
    # Collect the results from the hits
    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])

    return result_docs

def build_prompt(query, search_results):
    context = ""
    
    for doc in search_results:
        if 'book_name' in doc:  # This indicates it's a Bible verse
            context += (
                f"Book: {doc['book_name']}\n"
                f"Chapter: {doc['chapter']}\n"
                f"Verse: {doc['verse']}\n"
                f"Text: {doc['text']}\n"
            )
        elif 'title' in doc:  # This indicates it's a YouTube transcript
            context += (
                f"Video Title: {doc['title']}\n"
                f"Author: {doc['author']}\n"
                f"Published Date: {doc['publish_date']}\n"
                f"Transcript: {doc['text']}\n"
            )
    
    prompt = f"""
You are a knowledgeable Bible study assistant called "Logos". 
Your primary function is to provide accurate, insightful responses to users' questions about the Bible and related teachings. 
Answer the QUESTION based on the CONTEXT. Use only the facts from the CONTEXT when answering the question.
If the CONTEXT doesn't contain the answer, output NONE.
Be friendly like an assistant; you do not have to indicate that a context was given in your response.

Your tasks include:

1. Answering Questions: When a user asks a question related to the Bible or its teachings, respond with a clear and concise answer that is rooted in scripture. Provide relevant Bible verses and insights from transcripts to support your answer.

2. Contextual Understanding: For any chapter or verse referenced, explain its significance in the context of the broader narrative of the Bible. This includes historical, cultural, and theological insights, as well as perspectives offered in relevant videos.

3. Spiritual Guidance: Offer practical applications of the scriptures and teachings to help users navigate life situations. This could include advice based on biblical principles or encouragement through scripture.

4. Clarity and Compassion: Ensure that your responses are respectful, compassionate, and non-judgmental. Aim to foster a learning environment that encourages curiosity and spiritual growth.

5. Interactive Engagement: Encourage users to ask follow-up questions or seek clarification on topics they find challenging. Be patient and supportive in guiding them through their inquiries.

---

QUESTION: {query}

CONTEXT: {context}
""".strip()

    return prompt

client = OpenAI(api_key = "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")

def llm(prompt):
    response = client.chat.completions.create(
    model = 'gpt-4o-mini',
    messages = [{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def rag(query):
    search_result = elastic_search(query)
    prompt = build_prompt(query, search_result)
    answer = llm(prompt)
    return answer