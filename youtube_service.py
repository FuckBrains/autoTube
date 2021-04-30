import random
import settings
import logging
import time 
from youtube_api import upload_video as upload_video_to_youtube, upload_thumbnail as upload_thumbnail_to_youtube, get_video_thumbnail
from thumbnail_generator_v2 import generate_thumbnail
from repository import get_game_current_number, update_game_current_number
from difflib import SequenceMatcher

emotes = ['🔥', '⭐', '💀', '😈', '🙀', '⚡', '🏆', '🎮', '💣', '💎', '✅', '♠']


def generate_title(game, first_clip_title, current_number, top_3_streamers):
    title = ''
    random_emote = random.choice(emotes)
    first_streamer_part = ' ' + top_3_streamers[0] + ' '
    for word in first_clip_title.split(' '):
        ratio = SequenceMatcher(None, top_3_streamers[0], word).ratio()
        if ratio >= 0.5:
            first_streamer_part = ' '
            break
    title = random_emote + first_streamer_part + first_clip_title.replace('!', '').replace('.', '').upper() + '!' + ' ' + random_emote + ' ' + game['title_tail'] + ' #' + str(current_number)
    title = title.title()
    return title

def generate_chapters_section(streamer_names, clip_durations):
    seconds = 0
    minuts = 0
    chapters_lines = '_____________________________\n\n\n'
    for index, duration in enumerate(clip_durations):
        seconds_string = str(seconds) if len(str(seconds)) == 2 else '0' + str(seconds)
        minuts_string = str(minuts) if len(str(minuts)) == 2 else '0' + str(minuts)
        chapters_lines += minuts_string + ':' + seconds_string + ' ' + streamer_names[index] + '\n'
        seconds += round(duration)
        if seconds >= 60:
            seconds = seconds - 60
            minuts += 1
    return chapters_lines     


def generate_streamer_links_section(streamer_names):
    link_lines = 'CLIPS de los siguientes STREAMERS:\n\n'
    links = []
    for name in streamer_names:
        links.append('https://www.twitch.tv/' + name + '\n\n')
    links = set(links)
    link_lines += ''.join(links)    
    return link_lines

def generate_description(game, title, tags, streamer_names, clip_durations):
    return game['description'] + '\n\n\n' + title + '\n\n\n' + generate_streamer_links_section(streamer_names) + '\n' + generate_chapters_section(streamer_names, clip_durations)  + '\n\n' + ', '.join(tags)

def upload_video(game, first_clip_title, top_3_streamers, streamer_names, clip_durations):
    file_path = settings.RESULT_DIRECTORY + 'result.mp4'
    current_number = get_game_current_number(game['key']) + 1
    tags = game['tags'] + top_3_streamers
    title = generate_title(game, first_clip_title, current_number, top_3_streamers)
    description = generate_description(game, title, tags, streamer_names, clip_durations)
    category = game['category']
    fallback_title = game['game_name'] + ' - ' + game['title_tail'] + ' #' + str(current_number)
    video_id = None
    tries = 0
    logging.info(title)
    while video_id == None and tries < 5:
        video_id = upload_video_to_youtube(game, title, file_path, description, category, tags, fallback_title)
        tries = tries + 1
        time.sleep(30)
    update_game_current_number(game['key'], current_number)
    if video_id:
        upload_thumbnail(game, current_number, video_id)
    return video_id

def upload_thumbnail(game, current_number, video_id):
    tries = 0
    thumbnail_url = None
    while thumbnail_url == None and tries < 5:
        try:
            time.sleep(600)
            thumbnail_url = get_video_thumbnail(video_id)
            logging.info('thumbnail URL: ' + thumbnail_url)
            generate_thumbnail(game, current_number, thumbnail_url)
            logging.info('Thumbnail generated')
        except KeyError:
            logging.warning('Maxres thumbnail not found.')
        tries = tries + 1        
    upload_thumbnail_to_youtube(game, video_id, settings.DOWNLOADS_DIRECTORY + 'thumbnail.png')

