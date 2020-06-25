from youtube_api import upload_video as upload_video_to_youtube
import settings
import sqlite3
from repository import get_game_current_number, update_game_current_number

# game = settings.GAMES['lol_es']
# title = 'Test title'
# file_path = '/home/jorge/IdeaProjects/autoTube/test_video.mp4'
# description = 'test description'
# category = 20
# tags = ['test tag']

# upload_video_to_youtube(game, title, file_path, description, category, tags)

# conn = sqlite3.connect('database.db')
# sql = ''' INSERT INTO video_numbers(game_key,current_number)
#               VALUES(?,?) '''
# c = conn.cursor()
# task1 = ('fortnite_en', 180)
# c.execute(sql, task1)
# conn.commit()
# conn.close()

# update_game_current_number('fortnite_en', 185)
current_number = get_game_current_number('fortnite_en')
print(current_number)
