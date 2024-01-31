import os
import assemblyai as aai
import pandas as pd

import datetime


ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY")


def generate_keywords_from_audio(episode_urls, n_episodes):
    episodes = episode_urls[:n_episodes]

    transcriber = aai.Transcriber()

    print("Starting transcription...")
    start = datetime.datetime.now()

    transcript_group = transcriber.transcribe_group(
        episodes, 
        config=aai.TranscriptionConfig(auto_highlights=True)
    )

    stop = datetime.datetime.now()
    transcription_duration = stop - start
    print(f"{n_episodes} transcribed in {transcription_duration}")

    return transcript_group


def generate_analysis(transcript_group, episode_info):
    all_episodes_keywords = pd.DataFrame()

    for transcript in transcript_group:
        key_phrases_list = get_key_phrases(transcript)

        # key_phrases_list = "audio_url", "text", "rank", "start", "end"
        # episode_info = "title", "description", "date", "audio_url", "episode_length"

        key_phrases_df = pd.DataFrame(key_phrases_list)

        all_episodes_keywords = all_episodes_keywords.append(
            key_phrases_df, ignore_index=True
        )

    episode_info_df = pd.DataFrame(episode_info)

    keyword_analysis = all_episodes_keywords.merge(episode_info_df, on="audio_url", how="left")
    keyword_analysis = keyword_analysis.drop(["start", "end", "rank"], axis=1).drop_duplicates()

    keyword_analysis.to_csv("keyword_analysis.csv")

    return keyword_analysis


def get_key_phrases(transcript):
    key_phrases = []
    for phrase in transcript.auto_highlights.results:
        for timestamp in phrase.timestamps:
            key_phrases_dict = {
                "audio_url": transcript.audio_url,
                "text": phrase.text,
                "rank": phrase.rank,
                "start": timestamp.start,
                "end": timestamp.end,
            }
            key_phrases.append(key_phrases_dict)

    return key_phrases
