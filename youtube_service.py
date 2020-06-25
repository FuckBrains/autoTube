import random
import settings
import logging
from youtube_api import upload_video as upload_video_to_youtube, upload_thumbnail as upload_thumbnail_to_youtube
from thumbnail_generator import generate_thumbnail
from repository import get_game_current_number, update_game_current_number

emotes = ['🔥', '⭐', '💀', '📹', '😈', '🙀', '⚡', '🏆', '🎮', '💣', '💎', '✅', '♠']


def upload_video(game, first_clip_title, top_3_streamers):
    file_path = settings.RESULT_DIRECTORY + 'result.mp4'
    random_emote = random.choice(emotes)
    current_number = get_game_current_number(game['key']) + 1
    filtered_streamers = set(top_3_streamers)
    title = random_emote + ' ' + first_clip_title.title().replace('!', '').replace('.',
                                                                                   '').upper() + '!' + ' ' + random_emote + game['title_tail'] + ' #' + str(current_number)  + ' Ft. ' + ', '.join(filtered_streamers)
    tags = game['tags'] + top_3_streamers
    description = game['description'] + '\n\n\n' + title + '\n\n\n' + ', '.join(tags)
    category = game['category']
    
    video_id = upload_video_to_youtube(game, title, file_path, description, category, tags)
    update_game_current_number(game['key'], current_number)
    return video_id

def upload_thumbnail(game, video_id, streamer_name, title):
    try:
        generate_thumbnail(streamer_name, title)
        logging.info('Thumbnail generated')
    except ResourceWarning as e:
        message = 'Remove bg API failed. Thumbnail not created.'
        logging.warning(str(e))
        logging.warning(message)
        print(str(e), message)

    upload_thumbnail_to_youtube(game, video_id, settings.DOWNLOADS_DIRECTORY + 'thumbnail.png')    