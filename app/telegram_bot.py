import os
import openai
from openai import OpenAI
from elasticsearch import Elasticsearch
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Initialize Elasticsearch client
es_client = Elasticsearch("http://localhost:9200")

# Define your functions
def elastic_search(query, index_name="final_db"):
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "should": [
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
                            "fields": ["title", "text", "author"],
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
        if 'book_name' in doc:
            context += (
                f"**Book:** {doc['book_name']}\n"
                f"**Chapter:** {doc['chapter']}\n"
                f"**Verse:** {doc['verse']}\n"
                f"**Text:** {doc['text']}\n"
            )
        elif 'title' in doc:
            context += (
                f"**Video Title:** {doc['title']}\n"
                f"**Author:** {doc['author']}\n"
                f"**Published Date:** {doc['publish_date']}\n"
                f"**Transcript:** {doc['text']}\n"
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

**QUESTION:** {query}

**CONTEXT:** {context}
""".strip()

    return prompt

client = OpenAI()

def llm(prompt):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def rag(query):
    search_result = elastic_search(query)
    prompt = build_prompt(query, search_result)
    answer = llm(prompt)
    return answer

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome to the Bible Study Assistant! Ask your question about the Bible:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    answer = rag(user_input)
    await update.message.reply_text(answer)

def main():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN") # Replace with your bot token
    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
