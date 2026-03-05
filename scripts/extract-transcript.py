#!/usr/bin/env python3
"""
Extract YouTube video transcript
Usage: ./extract-transcript.py VIDEO_ID [LANGUAGE_CODE]
Compatible with youtube-transcript-api v1.x
"""

import sys
from youtube_transcript_api import YouTubeTranscriptApi

def extract_transcript(video_id, language='en'):
    """Extract transcript from YouTube video"""
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=[language, 'en'])
        full_text = " ".join([entry.text for entry in transcript])
        return full_text
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def list_available_transcripts(video_id):
    """List all available transcripts for a video"""
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)
        print(f"Available transcripts for {video_id}:")
        for t in transcript_list:
            print(f"  - {t.language} ({t.language_code})")
        return True
    except Exception as e:
        print(f"Error listing transcripts: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./extract-transcript.py VIDEO_ID [LANGUAGE_CODE]")
        print("       ./extract-transcript.py VIDEO_ID --list")
        sys.exit(1)

    video_id = sys.argv[1]

    if len(sys.argv) > 2 and sys.argv[2] == "--list":
        success = list_available_transcripts(video_id)
        sys.exit(0 if success else 1)

    language = sys.argv[2] if len(sys.argv) > 2 else 'en'
    transcript = extract_transcript(video_id, language)
    print(transcript)
