import schedule
import time
from twitch_clips import get_clips_by_lang
from video_edition import edit_video
from youtube import upload_video
from cleaning import clean_files


def job():
    clips, first_title = get_clips_by_lang('all')
    edit_video(clips)
    upload_video('title test')
    clean_files()

schedule.every().day.at("15:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
