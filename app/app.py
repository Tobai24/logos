import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import openai

# Initialize the Elasticsearch client and the embedding model
es_client = Elasticsearch("http://localhost:9200")
model = SentenceTransformer("all-mpnet-base-v2")

# Function for semantic search using Elasticsearch
def semantic_search(es_client, index_name, embedding_vector):
    # Construct the search query
    search_query = {
        "size": 10,  # Limit the number of results
        "knn": {
            "field": "text_vector",  # Field containing the dense vector
            "query_vector": embedding_vector,  # The query vector (embedding)
            "k": 10,  # Number of nearest neighbors to retrieve
            "num_candidates": 1000  # Candidate pool size for efficiency
        }
    }

    # Execute the search query
    response = es_client.search(index=index_name, body=search_query)
    
    result_docs = []
    # Collect and return the results from the hits
    result_docs = [hit['_source'] for hit in response['hits']['hits']]
    return result_docs

# Function to get the embedding vector of the user's question and perform a semantic search
def question_vector_knn(question, index_name="vector_db"):
    embedding_vector = model.encode(question)
    return semantic_search(es_client, index_name, embedding_vector)

# Function to build the prompt for the LLM
def build_prompt(query, search_results):
    context = ""
    
    for doc in search_results:
        if 'book_name' in doc:  # This indicates it's a Bible verse
            context += (
                f"**Book:** {doc['book_name']}\n"
                f"**Chapter:** {doc['chapter']}\n"
                f"**Verse:** {doc['verse']}\n"
                f"**Text:** {doc['text']}\n"
            )
        elif 'title' in doc:  # This indicates it's a YouTube transcript
            context += (
                f"**Video Title:** {doc['title']}\n"
                f"**Author:** {doc['author']}\n"
                f"**Published Date:** {doc['publish_date']}\n"
                f"**Transcript:** {doc['text']}\n"
            )
    
    
    prompt = f"""
    You are a knowledgeable Bible study assistant called "Logos". 
    Your primary function is to provide accurate, insightful responses to users' questions about the Bible and related teachings.
    Answer the QUESTION based on the CONTEXT provided. If necessary, use general Bible knowledge. 
    If you use external information, kindly inform the user.
    Please give the supporting bible verse for every answer you give.

    **QUESTION:** {query}

    **CONTEXT:** {context}
    """.strip()
    return prompt

# Function to generate a response from the LLM
client = openai.OpenAI()
def llm(prompt):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# RAG process: combining retrieval and generation
def rag(query):
    search_result = question_vector_knn(query)
    prompt = build_prompt(query, search_result)
    answer = llm(prompt)
    return answer

# Streamlit App UI
st.set_page_config(page_title="Bible Study Assistant", page_icon="📜")

# CSS styling for colors and font based on a more mature aesthetic
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    .stApp {
        background-color:  #E6F0FF; /* Soft light background */
        color: #002244 ; /* Darker text for contrast */
        font-family: 'Roboto', sans-serif; /* Roboto font */
    }
    .stTextInput, .stTextArea {
        background-color: #ffffff; /* White input fields */
        color: #333333; /* Dark text */
        border: 1px solid #cccccc; /* Light gray border */
        border-radius: 8px; /* Rounded corners */
        padding: 12px; /* Padding for comfort */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    }
    
    .stTextInput, .stTextArea {
        border: 1px solid #cccccc; /* Light gray border */
    }

    .stButton button {
        color: #F0F0F0;
        background-color: #336699;
        border-radius: 9px;
        font-size: 16px;
        padding: 10px 20px;
        transition: background-color 0.3s;
    }
    .stButton button:hover {
        background-color: #005599;
    }

    .previous-conversation {
        background-color: #f7f7f7; /* Light gray for previous conversations */
        padding: 15px;
        border-radius: 10px; /* Rounded corners */
        margin-bottom: 20px; /* Spacing below previous conversation */
        overflow-y: auto; /* Allow scrolling if content is too long */
        max-height: 400px; /* Limit height */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    }
    h1 {
        font-family: 'Roboto', serif;
        color: #F0F0F0; 
        text-align: center; 
    }
    .intro-section {
        padding: 20px;
        border-radius: 10px;
        color: #F0F0F0;
        background-color: #336699;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="intro-section">
    <h1>Welcome to Logos: Your Bible Study Assistant 📖</h1>
    <p>
        Logos is designed to guide you through thoughtful and engaging Bible study. This app contains comprehensive information from the entire Bible 📜 as well as transcripts from all Bible Project videos 🎥, offering rich insights into scripture and biblical teachings.
    </p>
    <p>
        With Logos, you can:
    </p>
    <ul>
        <li>Ask questions about Bible verses, chapters, or themes and get detailed explanations based on scripture ✨.</li>
        <li>Explore the context, meaning, and applications of various passages 🔍.</li>
        <li>Engage with insights from Bible Project transcripts to deepen your understanding 📖.</li>
    </ul>
    <p>
        You can ask about specific Bible verses or general questions ❓, and Logos will retrieve relevant information from both the Bible and the video transcripts to answer your questions 📚.
    </p>
    <p>
        Start by typing your question in the field below ⬇️, and you’ll be able to see your previous conversation as well 💬.
    </p>
    </div>

    """,
    unsafe_allow_html=True
)


# Initialize previous conversation storage
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
    
# Initialize user input storage
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Display previous conversations
if st.session_state.conversation:
    st.subheader("Previous Conversations:")
    conversation_container = st.container()
    with conversation_container:
        for idx, (q, a) in enumerate(st.session_state.conversation):
            st.markdown(f"**Question {idx + 1}:** {q}")
            st.markdown(f"**Answer {idx + 1}:** {a}")
            st.markdown("---")

# Input field for the user query
user_input = st.text_input("Ask your question about the Bible:", value=st.session_state.user_input, key="user_input_input")

# Submit button that can be activated by pressing Enter
if st.button("Submit") or (user_input and st.session_state.get('last_query') != user_input):
    if user_input:
        # Show loading message
        with st.spinner("Loading..."):
            answer = rag(user_input)

        # Store the conversation
        st.session_state.conversation.append((user_input, answer))
        
        # Display the answer
        st.markdown(f"**Answer:** {answer}")

        # Clear the input after submission
        st.session_state.user_input = ""  # Clear input in session state
        st.session_state.last_query = user_input  # Store the last query to check against new input
