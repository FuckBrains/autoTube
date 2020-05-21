import datetime
import logging
import settings
from twitch_clips import get_clips_by_lang
from video_edition import edit_video
from youtube import upload_video
from cleaning import clean_files

# clips = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# first_title = 'RandomTitle'


def setup():
    logging.basicConfig(filename=settings.LOGS_DIRECTORY + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log', level=logging.INFO,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Started')


if settings.ENVIRONMENT == 'production':
    setup()
logging.info('Starting to clean the files')
clean_files()

clips, first_title = get_clips_by_lang('all')
edit_video(clips)
upload_video(first_title)
