from twitch_clips import get_clips_by_lang
from video_edition import edit_video
from youtube import upload_video
from cleaning import clean_files

# clips = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

clips, first_title = get_clips_by_lang('all')
edit_video(clips)
upload_video('title test')
clean_files()

