import os
import xml.etree.ElementTree as ET
from mutagen.mp3 import MP3
from datetime import timedelta

def get_audio_info(filename):
    audio = MP3(filename)
    length = os.path.getsize(filename)
    duration = int(audio.info.length)
    return length, duration

def format_duration(seconds):
    return str(timedelta(seconds=seconds)).split('.')[0].zfill(8)

def create_rss_xml(podcast_info, episodes):
    rss = ET.Element("rss", {
        "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
        "version": "2.0"
    })
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = podcast_info['title']
    
    owner = ET.SubElement(channel, "itunes:owner")
    ET.SubElement(owner, "itunes:email").text = "test@gmail.com"
    
    ET.SubElement(channel, "itunes:author").text = podcast_info['author']
    ET.SubElement(channel, "description").text = podcast_info['description']
    
    image = ET.SubElement(channel, "itunes:image")
    image.set("href", podcast_info['cover_image'])
    
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "link").text = podcast_info['link']

    for episode in episodes:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = episode['title']
        ET.SubElement(item, "description")
        ET.SubElement(item, "pubDate")
        enclosure = ET.SubElement(item, "enclosure")
        enclosure.set("url", f"{podcast_info['base_url']}/files/{episode['filename']}")
        enclosure.set("type", "audio/mpeg")
        enclosure.set("length", str(episode['length']))
        ET.SubElement(item, "itunes:duration").text = episode['duration']

    return ET.tostring(rss, encoding="unicode", xml_declaration=True)

def main():
    podcast_info = {
        'title': input("Enter the Title of the Podcast: "),
        'author': input("Enter the Podcast Author: "),
        'description': input("Enter the Podcast Description: "),
        'cover_image': input("Enter the Podcast Cover Image URL: "),
        'link': input("Enter the Podcast Link: "),
        'base_url': input("Enter the Base URL of episodes: ")
    }

    episodes = []
    audio_files = sorted([f for f in os.listdir() if f.endswith('.mp3')])

    for file in audio_files:
        title = os.path.splitext(file)[0]
        length, duration_seconds = get_audio_info(file)
        duration = format_duration(duration_seconds)

        episodes.append({
            'title': title,
            'filename': file,
            'length': length,
            'duration': duration
        })

    rss_xml = create_rss_xml(podcast_info, episodes)
    
    with open('podcast_rss.xml', 'w', encoding='utf-8') as f:
        f.write(rss_xml)

    print("RSS XML file 'podcast_rss.xml' has been created.")

if __name__ == "__main__":
    main()
