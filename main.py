from collect_audio import collect_episode_urls
from collect_key_phrases import *

rss_feed = "https://feeds.megaphone.fm/hubermanlab"
n_episodes = 10

episode_urls, episode_info = collect_episode_urls(rss_feed)

transcript_group = generate_keywords_from_audio(episode_urls, n_episodes)

all_keywords = generate_analysis(transcript_group, episode_info)

print(all_keywords)
