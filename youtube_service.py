import random
import settings
import logging
from youtube_api import upload_video as upload_video_to_youtube, upload_thumbnail as upload_thumbnail_to_youtube
from thumbnail_generator import generate_thumbnail

emotes = ['🔥', '⭐', '💀', '📹', '😈', '🙀', '⚡', '🏆', '🎮', '💣', '💎', '✅', '♠']


def upload_video(game, first_clip_title):
    file_path = settings.RESULT_DIRECTORY + 'result.mp4'
    random_emote = random.choice(emotes)
    game_dict = settings[game]
    title = random_emote + ' ' + first_clip_title.title().replace('!', '').replace('.',
                                                                                   '').upper() + '!' + ' ' + random_emote + game_dict['title_tail']
    description = game_dict['description']
    category = game_dict['category']
    tags = game_dict['tags']
    video_id = upload_video_to_youtube(game, title, file_path, description, category, tags)
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