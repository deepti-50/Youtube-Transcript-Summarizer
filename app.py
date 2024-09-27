import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from googletrans import Translator
import cv2  # OpenCV for video frame extraction
import pafy  # Library for downloading YouTube videos

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Translator for multi-language support
translator = Translator()

# Extract video ID from YouTube URL
def extract_video_id(youtube_url):
    query = urlparse(youtube_url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    elif query.hostname in ['www.youtube.com', 'youtube.com']:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        elif query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None

@st.cache_data
def extract_transcript_details(youtube_video_url):
    try:
        video_id = extract_video_id(youtube_video_url)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i['text'] for i in transcript_text])
        return transcript
    except Exception as e:
        return None

# Translate text to target language
def translate_text(text, target_language):
    try:
        translated_text = translator.translate(text, dest=target_language).text
        return translated_text
    except Exception as e:
        return f"Translation failed: {str(e)}"

# Generate summary based on user-selected detail level
def generate_gemini_content(transcript_text, prompt, summary_length):
    try:
        model = genai.GenerativeModel("gemini-pro")
        
        # Modify prompt based on summary length
        if summary_length == 'Detailed (50%)':
            prompt += " Summarize in detail and provide the most important points, within 400 words."
        elif summary_length == 'Medium (25%)':
            prompt += " Summarize with moderate detail, within 250 words."
        else:
            prompt += " Provide a very concise summary, within 100 words."
        
        response = model.generate_content(prompt + transcript_text)
        return response.text if response else "No summary could be generated."
    except Exception as e:
        return f"Error in generating content: {str(e)}"

# Extract keyframes from video using OpenCV
def extract_keyframes(video_url, num_keyframes=5):
    keyframes = []
    try:
        # Download video using pafy
        video = pafy.new(video_url)
        best = video.getbest(preftype="mp4")

        cap = cv2.VideoCapture(best.url)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_interval = total_frames // num_keyframes

        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if count % frame_interval == 0:
                keyframes.append(frame)
            count += 1
        cap.release()
        return keyframes
    except Exception as e:
        return []

# Streamlit App UI
st.title("YouTube Transcript to Detailed Notes Converter with Visual Summary")
youtube_link = st.text_input("Enter YouTube Video Link:")

# Language selection
languages = {
    'English': 'en',
    'हिन्दी (Hindi)': 'hi',
    'Español (Spanish)': 'es',
    'Français (French)': 'fr',
    'Deutsch (German)': 'de',
    '中文 (Chinese)': 'zh-cn',
    '日本語 (Japanese)': 'ja',
    'العربية (Arabic)': 'ar'
}

target_language = st.selectbox("Select Language for Summary", list(languages.keys()))

# Summary length selection
summary_length_options = ['Concise (10%)', 'Medium (25%)', 'Detailed (50%)']
summary_length = st.selectbox("Select Summary Length", summary_length_options)

# Define prompt for summarization
prompt = """
You are a YouTube video summarizer. You will take the transcript text
and summarize the entire video, providing the important points
based on the requested summary length. Please summarize the text: 
"""

if youtube_link:
    video_id = extract_video_id(youtube_link)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    with st.spinner("Fetching transcript..."):
        transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        with st.spinner("Generating summary..."):
            # Step 1: Generate summary in English with selected summary length
            summary_in_english = generate_gemini_content(transcript_text, prompt, summary_length)

        if summary_in_english:
            # Step 2: Translate summary if a non-English language is selected
            lang_code = languages[target_language]
            if lang_code != 'en':
                with st.spinner(f"Translating summary to {target_language}..."):
                    translated_summary = translate_text(summary_in_english, lang_code)
                    st.markdown(f"## Detailed Notes in {target_language}:")
                    st.write(translated_summary)
            else:
                # Display summary in English
                st.markdown("## Detailed Notes in English:")
                st.write(summary_in_english)

            # Step 3: Extract and display keyframes
            with st.spinner("Extracting keyframes..."):
                keyframes = extract_keyframes(youtube_link, num_keyframes=5)
                if keyframes:
                    st.markdown("## Key Visual Highlights:")
                    for i, keyframe in enumerate(keyframes):
                        st.image(keyframe, caption=f"Keyframe {i+1}", use_column_width=True)
                else:
                    st.error("Could not extract keyframes.")
        else:
            st.error("Could not generate summary. Please try again.")
    else:
        st.error("Could not retrieve transcript. Please check the video URL or try again later.")
