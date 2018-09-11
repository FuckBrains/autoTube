import urllib.request
import requests
import sys
from moviepy.editor import *
from settings import CLIENTID

base_clip_path = 'https://clips-media-assets2.twitch.tv/'
headers = {
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Client-ID': CLIENTID,
    'User-Agent': 'Mozilla/5.0'
}


def retrieve_mp4_data(slug):
    print("https://api.twitch.tv/helix/clips?id=" + slug)
    clip_info = requests.get(
        "https://api.twitch.tv/helix/clips?id=" + slug,
        headers={"Client-ID": CLIENTID}).json()
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
def get_clip(clip, broadcaster, position):
    slug = clip.split('/')[3].split('?')[0].replace('\n', '')
    mp4_url = retrieve_mp4_data(slug)
    output_path = 'downloads/' + str(position) + ".mp4"

    print('\nDownloading clip slug: ' + slug)
    print(mp4_url)
    urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
    return VideoFileClip(output_path).duration


def get_clips_by_lang(lang):
    if lang != 'all':
        lang_request = '&language=' + lang
    else:
        lang_request = ''
    print('Downloading TOP 30 last 24h ' + lang + ' Fortnite clips')

    response = requests.get('https://api.twitch.tv/kraken/clips/top?game=' + 'Fortnite' +
                            '&period=' + 'day' +
                            '&limit=' + '100' +
                            lang_request, headers=headers)

    result = []
    first_title = ""
    complete_duration = 0
    for i, clip in enumerate(response.json()['clips']):
        try:
            print(clip['url'])
            print(clip['broadcaster']['name'])
            if i == 0:
                first_title = clip['title']
            clip_duration = get_clip(clip['url'], clip['broadcaster']['name'], i)
            complete_duration += clip_duration
            result.append(clip['broadcaster']['name'])
            if complete_duration >= 585:
                break
        except:
            pass
    print('Download finished')
    return result, first_title
