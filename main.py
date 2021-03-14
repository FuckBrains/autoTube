import datetime
import logging
import settings
import game_config
import sentry_sdk
import argparse
from twitch_api import get_clips_by_lang
from video_edition import edit_video
from youtube_service import upload_video
from cleaning import clean_files

# clips = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# clips = ['0', '1']
# clips = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
# first_title = 'RandomTitle'
# video_id = 'yCOSJT_xTAc'
# first_clip_title = 'MIS TATUAJES!'
# first_streamer = 'peereira7'

def setup():
    logging.basicConfig(filename=settings.LOGS_DIRECTORY + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log', level=logging.INFO,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Started')
    sentry_sdk.init("https://a4e938ae150e45dbbb6c4b1ac61d96a7@o410550.ingest.sentry.io/5284600")


def generate_video(game_key):
    logging.info('Starting to clean the files')
    clean_files()
    logging.info('Files cleaned')
    game = game_config.GAMES[game_key]
    clips, first_clip_title = get_clips_by_lang(game)
    edit_video(clips)
    video_id = upload_video(game, first_clip_title)

if settings.ENVIRONMENT == 'production':
    setup()
parser = argparse.ArgumentParser(description='Process game key.')
parser.add_argument('--game')
args = parser.parse_args()
if args.game in game_config.GAMES.keys():
    generate_video(args.game)
else:
    print(args.game, 'not a valid game')    
