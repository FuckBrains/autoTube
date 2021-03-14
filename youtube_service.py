import random
import settings
import logging
import time 
from youtube_api import upload_video as upload_video_to_youtube, upload_thumbnail as upload_thumbnail_to_youtube, get_video_thumbnail
from thumbnail_generator_v2 import generate_thumbnail
from repository import get_game_current_number, update_game_current_number

emotes = ['🔥', '⭐', '💀', '😈', '🙀', '⚡', '🏆', '🎮', '💣', '💎', '✅', '♠']


def upload_video(game, first_clip_title):
    file_path = settings.RESULT_DIRECTORY + 'result.mp4'
    random_emote = random.choice(emotes)
    current_number = get_game_current_number(game['key']) + 1
    title = random_emote + ' ' + first_clip_title.title().replace('!', '').replace('.',
                                                                                   '').upper() + '!' + ' ' + random_emote + game['title_tail'] + ' #' + str(current_number)
    tags = game['tags'] + top_3_streamers
    description = game['description'] + '\n\n\n' + title + '\n\n\n' + ', '.join(tags)
    category = game['category']
    fallback_title = game['game_name'] + game['title_tail'] + ' #' + str(current_number)
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

