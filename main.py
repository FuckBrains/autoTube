import datetime
import logging
import settings
from twitch_clips import get_clips_by_lang
from video_edition import edit_video
from youtube import upload_video
from cleaning import clean_files

# clips = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def setup():
    logging.basicConfig(filename=settings.LOGS_DIRECTORY + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log', level=logging.INFO,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Started')


setup()
need_to_clear = False
try:
    clips, first_title = get_clips_by_lang('all')
    need_to_clear = True
except Exception as e:
    logging.error(str(e))
try:
    edit_video(clips)
except Exception as e:
    logging.error(str(e))
try:
    upload_video(datetime.datetime.now().strftime('%Y-%m-%d'))
except Exception as e:
    logging.error(str(e))
try:
    if need_to_clear:
        clean_files()
except Exception as e:
    logging.error(str(e))

