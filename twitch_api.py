import urllib.request
import requests
import sys
import logging
import settings
import time
from moviepy.editor import *
from settings import CLIENTID

base_clip_path = 'https://clips-media-assets2.twitch.tv/'
headers = {
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Client-ID': CLIENTID,
    'User-Agent': 'Mozilla/5.0'
}


def retrieve_mp4_data(twitch_oauthh_token, slug):
    print("https://api.twitch.tv/helix/clips?id=" + slug)
    clip_info = requests.get(
        "https://api.twitch.tv/helix/clips?id=" + slug,
        headers={"Client-ID": CLIENTID, "Authorization": 'Bearer ' + twitch_oauthh_token}).json()
    print(clip_info)
    thumb_url = clip_info['data'][0]['thumbnail_url']
    slice_point = thumb_url.index("-preview-")
    mp4_url = thumb_url[:slice_point] + '.mp4'
    return mp4_url


def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()


# for each clip in clips.txt
def get_clip(twitch_oauthh_token, clip, broadcaster, position):
    slug = clip.split('/')[3].split('?')[0].replace('\n', '')
    mp4_url = retrieve_mp4_data(twitch_oauthh_token, slug)
    output_path = settings.DOWNLOADS_DIRECTORY + str(position) + ".mp4"

    print('\nDownloading clip slug: ' + slug)
    print(mp4_url)
    urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
    clip = VideoFileClip(output_path)
    duration = clip.duration
    clip.close()
    return duration


def get_twitch_oauth_token():
    data = {
        "client_id": settings.CLIENTID,
        "client_secret": settings.TWITCH_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post('https://id.twitch.tv/oauth2/token', data)
    return response.json()['access_token']


def get_clips_by_lang(game):
    lang = game['language']
    lang_request = '&language=' + lang
    
    try:
        twitch_oauth_token = get_twitch_oauth_token()
        response = None
        responseHasClips = False
        tries = 0
        while responseHasClips == False and tries < 5:
            response = requests.get('https://api.twitch.tv/kraken/clips/top?game=' + game['game_name'] +
                                '&period=' + 'day' +
                                '&limit=' + '2' +
                                lang_request, headers=headers)
            responseHasClips = 'clips' in response.json()
            tries = tries + 1
            time.sleep(30)

        logging.info('Clips list info downloaded correctly')                        

    except Exception as e:
        logging.error(str(e))
    result = []
    first_title = ''
    top_3_streamers = []
    complete_duration = 0
    for i, clip in enumerate(response.json()['clips']):
        try:
            print(clip['url'])
            print(clip['broadcaster']['name'])
            if i == 0:
                first_title = clip['title']
            if i <= 2:
                top_3_streamers.append(clip['broadcaster']['name'])
            
            clip_duration = get_clip(twitch_oauth_token,
                                     clip['url'], clip['broadcaster']['name'], i)
            complete_duration += clip_duration
            result.append(clip['broadcaster']['name'])

            if complete_duration >= 585:
                break
        except Exception as e:
            logging.error(str(e))
    logging.info('Download finished')
    return result, first_title, top_3_streamers
