import os
import re
import json
import nltk
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from nltk.tokenize import word_tokenize

# Load API key from environment variable
API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_ID = 'UCVfwlh9XpX2Y_tQfjeln9QA'

# Ensure NLTK resources are downloaded
nltk.download('punkt')

# Function to append data to a JSON file
def append_to_json(video_data, filename='video_data.json'):
    if os.path.exists(filename):
        # Read the existing data from the file
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Append the new data
    existing_data.extend(video_data)  # Use extend to add multiple entries

    # Write the updated data back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    # Return the set of video IDs for later checks
    return {entry['video_id'] for entry in existing_data}

# Function to get all video URLs from the channel
def get_all_video_urls_from_channel(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    response = youtube.channels().list(part='contentDetails', id=channel_id).execute()
    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    video_urls = []
    next_page_token = None

    while True:
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in playlist_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_urls.append(video_url)

        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break

    return video_urls

# Extract video ID from URL
def extract_video_id(url):
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return video_id_match.group(1) if video_id_match else None

# Function to get video metadata using pytube
def get_video_metadata(video_url):
    yt = YouTube(video_url)
    
    # Safely handle cases where publish_date may be None
    publish_date = yt.publish_date.isoformat() if yt.publish_date else "Unknown"
    
    metadata = {
        "video_id": yt.video_id,
        "title": yt.title,
        "author": yt.author,
        "publish_date": publish_date
    }
    return metadata

# Function to get transcript using youtube-transcript-api
def get_video_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript  # Return full transcript, which contains start and duration

# Function to split transcripts into chunks based on token limit
def split_transcript(transcript_entries, token_limit=200):
    chunks = []
    current_chunk = []
    current_tokens = 0

    for entry in transcript_entries:
        entry_tokens = len(word_tokenize(entry['text']))
        
        # Check if adding this entry exceeds the token limit
        if current_tokens + entry_tokens > token_limit:
            # Save the current chunk and start a new one
            if current_chunk:  # Only save if there's content
                chunks.append(current_chunk)
                current_chunk = []
                current_tokens = 0
        
        current_chunk.append(entry)
        current_tokens += entry_tokens

    # Add any remaining entries in the last chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

# Function to check existing video IDs in JSON
def get_existing_video_ids(filename='video_data.json'):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            return {entry['video_id'] for entry in existing_data}
    return set()  # Return an empty set if the file doesn't exist

# Function to process videos and save data row by row, immediately appending to JSON
def process_videos_as_table(video_urls):
    existing_video_ids = get_existing_video_ids()  # Get already processed video IDs

    for url in video_urls:
        try:
            video_id = extract_video_id(url)
            if video_id:
                # Skip if the video ID is already processed
                if video_id in existing_video_ids:
                    print(f"Skipping already processed video: {url}")
                    continue

                metadata = get_video_metadata(url)
                transcript_entries = get_video_transcript(video_id)

                # Split the transcript into manageable chunks
                transcript_chunks = split_transcript(transcript_entries)

                # Prepare the video data structure
                video_data = []
                for chunk in transcript_chunks:
                    # Create a text summary for each chunk
                    text = ' '.join(entry['text'] for entry in chunk)
                    start = chunk[0]['start']
                    duration = sum(entry['duration'] for entry in chunk)
                    
                    video_data.append({
                        "video_id": metadata['video_id'],
                        "title": metadata['title'],
                        "publish_date": metadata['publish_date'],
                        "author": metadata['author'],
                        "text": text,
                        "start": start,
                        "duration": duration
                    })

                # Save the video data immediately to the JSON file
                append_to_json(video_data)
                
                print(f"Processed and saved video: {metadata['title']}")
            else:
                print(f"Could not extract video ID from URL: {url}")
        except Exception as e:
            print(f"Error processing video: {e}")

# Fetch all video URLs from the YouTube channel
video_urls = get_all_video_urls_from_channel(API_KEY, CHANNEL_ID)

# Process and save the data as soon as it's loaded
process_videos_as_table(video_urls)

