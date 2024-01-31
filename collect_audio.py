import feedparser
from datetime import timedelta

def collect_episode_urls(rss_feed):
    feed = feedparser.parse(rss_feed)

    episode_urls = []
    episode_info = []

    for entry in feed.entries:
        episode_dict = {
            "title": entry.title,
            "description": entry.subtitle,
            "date": entry.published,
            "audio_url": entry.links[1]["href"],
            "episode_length": str(timedelta(seconds=int(entry.itunes_duration))),
        }
        episode_info.append(episode_dict)

        episode_urls.append(entry.links[1]["href"])

    return episode_urls, episode_info