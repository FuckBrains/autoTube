import random
import settings
import logging
from youtube_api import upload_video as upload_video_to_youtube, upload_thumbnail as upload_thumbnail_to_youtube
from thumbnail_generator import generate_thumbnail

emotes = ['🔥', '⭐', '💀', '📹', '😈', '🙀', '⚡', '🏆', '🎮', '💣', '💎', '✅', '♠']


def upload_video(first_clip_title):
    file_path = settings.RESULT_DIRECTORY + 'result.mp4'
    random_emote = random.choice(emotes)
    title = random_emote + ' ' + first_clip_title.title().replace('!', '').replace('.',
                                                                                   '').upper() + '!' + ' ' + random_emote + ' - FORTNITE EPIC & FUNNY BEST MOMENTS'
    description = 'The best Fortnite Clips, WTF Moments & Epic Moments! ' \
        'Fortnite Fails, Wins, Best moments Funny Moments!' \
        'If you like it, please like and subscribe!'
    category = 20  # Gaming
    tags = ['fortnite', 'best', 'clips', 'moments', 'ninja', 'wins', 'fails', 'daily', 'like', 'wtf', 'highlights',
            'funny', 'plays', 'fortnite best', 'fortnite clips', 'fortnite moments', 'fortnite ninja',
            'fortnite wins', 'fortnite fails', 'fortnite daily', 'fortnite like', 'fortnite wtf',
            'fortnite highlights', 'epic', 'tfue', 'savage',
            'fortnite funny', 'fortnite plays']
    video_id = upload_video_to_youtube(title, file_path, description, category, tags)
    return video_id

def upload_thumbnail(video_id, streamer_name, title):
    try:
        generate_thumbnail(streamer_name, title)
        logging.info('Thumbnail generated')
    except ResourceWarning as e:
        message = 'Remove bg API failed. Thumbnail not created.'
        logging.warning(str(e))
        logging.warning(message)
        print(str(e), message)

    upload_thumbnail_to_youtube(video_id, settings.DOWNLOADS_DIRECTORY + 'thumbnail.png')    