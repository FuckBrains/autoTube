import random
import settings
from youtube_api import upload_video as upload_video_to_youtube

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
    upload_video_to_youtube(title, file_path, description, category, tags)