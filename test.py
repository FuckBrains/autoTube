from youtube_api import upload_video as upload_video_to_youtube
import game_config
import settings
import sqlite3
from repository import get_game_current_number, update_game_current_number
from youtube_service import upload_video, generate_title
from youtube_api import upload_video as upload_video_api, get_video_thumbnail
from thumbnail_generator_v2 import generate_thumbnail
from difflib import SequenceMatcher
from moviepy.editor import *

# update_game_current_number('ark_es', 4)
# current_number = get_game_current_number('fortnite_en')
# print(current_number)
game = game_config.GAMES['lol_es']
# upload_video(game, 'elmillor lo da todo', ['elmillor', 'coscu'])
# upload_video_api(game, 'test title', file_path, 'test description', 20, ['test tag'])
# thumbnail_url = get_video_thumbnail('8Kl0FmlagF0')
# generate_thumbnail(game, 202, thumbnail_url)
# clip = VideoFileClip('test_video.mp4')
# print(int(clip.duration))
title = generate_title(game, 'se la juega', 10, ['elmillor', 'werlyb', 'knekro'])

print(title)