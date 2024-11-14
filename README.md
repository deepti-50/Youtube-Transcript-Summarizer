# YouTube Transcript to Detailed Notes Converter with Visual Summary

This Streamlit application allows users to convert YouTube video transcripts into detailed notes with multi-language support. Users can generate summaries at different levels of detail, translate the summaries, and view visual highlights through keyframes extracted from the video.

## Features

- **YouTube Transcript Extraction**: Retrieves the transcript from a specified YouTube video.
- **Multi-Language Support**: Summaries can be translated into multiple languages.
- **Summary Generation**: Generates concise, medium, or detailed summaries using Google's Gemini AI.
- **Keyframe Extraction**: Provides a visual summary by extracting keyframes from the video.
- **Streamlit Interface**: Interactive UI for user inputs and outputs.

## Prerequisites

- Python 3.7 or higher
- YouTube Data API access
- Required API keys:
  - **Google Generative AI (Gemini API)** for generating summaries.
  - Ensure `.env` file contains `GOOGLE_API_KEY`.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the root directory:
     ```plaintext
     GOOGLE_API_KEY=your_google_api_key
     ```

4. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

## Code Overview

### `extract_video_id`
Extracts the video ID from a YouTube URL to fetch video data.

### `extract_transcript_details`
Retrieves the video transcript based on the YouTube video ID using the `YouTubeTranscriptApi` package.

### `translate_text`
Translates text to the user-selected language using Google Translate.

### `generate_gemini_content`
Generates a summary of the transcript based on the user’s selected detail level using Google's Gemini AI model.

### `extract_keyframes`
Extracts keyframes from the video for a visual summary, using OpenCV to process video frames.

### Streamlit UI
- **Video URL Input**: Users enter a YouTube URL.
- **Language and Summary Options**: Allows selection of language and detail level for the summary.
- **Output Display**: Shows the generated summary and visual keyframes.

## Usage

1. Enter a YouTube video link.
2. Choose the language for the summary.
3. Select the level of detail for the summary (Concise, Medium, Detailed).
4. Click **Get Detailed Notes** to generate the summary and keyframes.

## Dependencies

The application relies on the following key libraries:
- `streamlit`: For building the web UI.
- `google.generativeai`: For content generation using Gemini AI.
- `youtube_transcript_api`: To retrieve video transcripts.
- `googletrans`: For translating text.
- `pafy` and `cv2` (OpenCV): For video processing and keyframe extraction.

## Error Handling

The application includes error handling for:
- Transcript retrieval issues.
- Language translation failures.
- Content generation errors.
- Video and keyframe extraction issues.

## Limitations

- **YouTube API Limitations**: Transcript availability may vary based on video.
- **Translation Accuracy**: Google Translate may have limitations with some languages.

## Future Enhancements

- Support for additional AI models for more summary customization.
- Advanced keyframe selection based on scene changes.
- Expanded multi-language support with other translation APIs.
