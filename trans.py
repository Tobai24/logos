import re
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import json
import nltk

# Download NLTK data for sentence tokenization
nltk.download('punkt', quiet=True)

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
    return transcript_texts

# Function to split transcript into sentences using NLTK
def split_into_sentences(text):
    sentences = nltk.tokenize.sent_tokenize(text)
    return sentences

# Function to chunk sentences into blocks of 200 words each
def chunk_sentences(sentences, chunk_size=200):
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for sentence in sentences:
        sentence_word_count = len(sentence.split())
        if current_word_count + sentence_word_count > chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_word_count = sentence_word_count
        else:
            current_chunk.append(sentence)
            current_word_count += sentence_word_count
            
    if current_chunk:  # Add the last chunk if it exists
        chunks.append(" ".join(current_chunk))
    
    return chunks

# Function to create structured JSON block for each video
def create_json_block(metadata, transcript):
    transcript_text = " ".join(transcript)
    sentences = split_into_sentences(transcript_text)
    sentence_chunks = chunk_sentences(sentences)
    
    json_structure = {
        "video_id": metadata['video_id'],  # This will be set later
        "title": metadata['title'],
        "description": metadata['description'],
        "publish_date": metadata['publish_date'],
        "author": metadata['author'],
        "transcripts": [
            {
                "text": chunk,
                "chunk_index": index + 1,  # 1-based index
                "word_count": len(chunk.split()),
                "context": f"Context for chunk {index + 1}"  # You can customize this
            } for index, chunk in enumerate(sentence_chunks)
        ]
    }
    
    return json_structure

# Main function to process a list of YouTube URLs
def process_videos(video_urls):
    all_video_data = []
    
    for url in video_urls:
        try:
            video_id = extract_video_id(url)
            if video_id:
                metadata = get_video_metadata(url)
                transcript = get_video_transcript(video_id)
                
                # Include video_id in metadata
                metadata['video_id'] = video_id
                
                video_data = create_json_block(metadata, transcript)
                all_video_data.append(video_data)  # Append the video data directly
                print(f"Processed video: {metadata['title']}")
            else:
                print(f"Could not extract video ID from URL: {url}")
        except Exception as e:
            print(f"Error processing video: {e}")

    return all_video_data

# Save the processed data to a JSON file
def save_to_json_file(data, filename='videos_transcript.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data successfully saved to {filename}")

# Creating a Python list of the URLs from the input string
video_urls = [
    "https://youtu.be/ALsluAKBZ-c?si=6k-0eTAQGsVq0WjE",
    "https://youtu.be/GQI72THyO5I?si=Pa3O9TUPeR2v57qd",
    "https://youtu.be/F4isSyennFo?si=QcopgxV7kmdgQpij",
    "https://youtu.be/jH_aojNJM3E?si=iGBqLrhJQR1yJwKc",
    "https://youtu.be/oNpTha80yyE?si=R8gpLW9Qtzy7YdLd",
    "https://youtu.be/IJ-FekWUZzE?si=bvwKGbdPPrXSdSDB",
    "https://youtu.be/tp5MIrMZFqo?si=5k2QlTy37bFtuRCo",
    "https://youtu.be/q5QEH9bH8AU?si=WIK3l2LskCaueiGd",
    "https://youtu.be/JqOqJlFF_eU?si=DrgAOi5Oie1odhxg",
    "https://youtu.be/kOYy8iCfIJ4?si=JIRwHJdKQ8f7rZ0w",
    "https://youtu.be/kOYy8iCfIJ4?si=ApttcZ33RiJM1sg2",
    "https://youtu.be/YvoWDXNDJgs?si=jm-SGfan5wJhB05N",
    "https://youtu.be/bVFW3wbi9pk?si=HTi3RFxfAiTowwzQ",
    "https://youtu.be/d0A6Uchb1F8?si=S1YiEMdgwq2w6O6P",
    "https://youtu.be/_TzdEPuqgQg?si=NuQ78-syZeDw_e56",
    "https://youtu.be/RSK36cHbrk0?si=H2NOZddzWmsE-2IL",
    "https://youtu.be/R-CIPu1nko8?si=xd28knt-IvWWUxQw",
    "https://youtu.be/SDeCWW_Bnyw?si=42ps5IUjXWxZ7ctr",
    "https://youtu.be/kE6SZ1ogOVU?si=9TD1Gqo89fnxQHcl",
    "https://youtu.be/zQLazbgz90c?si=EG-yV9Hd8rEKuyYZ",
    "https://youtu.be/mGgWaPGpGz4?si=k6byodG5sbBqSdWF",
    "https://youtu.be/i4ogCrEoG5s?si=cc1RuBezKlT50s8Y",
    "https://youtu.be/dLIabZc0O4c?si=NmVo6g_AMxhcrW0p",
    "https://youtu.be/MFEUEcylwLc?si=i2WANz7PccQPiTSz",
    "https://youtu.be/Y30DanA5EhU?si=6ltWI0hMe_KeoDJJ",
    "https://youtu.be/OPMaRqGJPUU?si=KQw5XN0ZXGcbuZgX",
    "https://youtu.be/oFZknKPNvz8?si=YixbGCCiaBlkDYzQ",
    "https://youtu.be/juPvv_xcX-U?si=BeCAHZsingpa9KSX",
    "https://youtu.be/_106IfO6Kc0?si=Bn_z3x6lDbERD-fY",
    "https://youtu.be/HPGShWZ4Jvk?si=6mlsvUtyHnLPKgl8",
    "https://youtu.be/j9phNEaPrv8?si=n2yCIX1FskuM7SlD",
    "https://youtu.be/AzmYV8GNAIM?si=eeoolXmemCdfvzK4",
    "https://youtu.be/xQwnH8th_fs?si=EOT71JM_f3IQqUWc",
    "https://youtu.be/4KC7xE4fgOw?si=ijpcDZk7DJvrh5de",
    "https://youtu.be/0h1eoBeR4Jk?si=Y_1qAyTNWF2X8uf-",
    "https://youtu.be/p8GDFPdaQZQ?si=yK_FR2j2SuphOAtW",
    "https://youtu.be/lrsQ1tc-2wk?si=fOT0TAhgvsT3EOCO",
    "https://youtu.be/JydNSlufRIs?si=02HewRDINWKuiKLe",
    "https://youtu.be/9cSC9uobtPM?si=VNbN_iYL0SjMFJ7R",
    "https://youtu.be/MkETkRv9tG8?si=fHYzrEzbQxaAAtUc",
    "https://youtu.be/HR7xaHv3Ias?si=cmrKqcvSYdVAITAD",
    "https://youtu.be/GswSg2ohqmA?si=odrS2g8pK9LEUkw1",
    "https://youtu.be/VeUiuSK81-0?si=SYqZTgfPhQTYb06z",
    "https://youtu.be/Gab04dPs_uA?si=8heULe65FoI-Y86V"
]

# Process the videos and save the results into a JSON file
processed_data = process_videos(video_urls)
save_to_json_file(processed_data, 'videos_transcript.json')


