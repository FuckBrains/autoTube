import httplib2
import http.client as httplib
import os
import sys
import time
import logging
import settings
import game_config

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
                        httplib.IncompleteRead, httplib.ImproperConnectionState,
                        httplib.CannotSendRequest, httplib.CannotSendHeader,
                        httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google Developers Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   

with information from the Developers Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
"""

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
SCOPES = ['https://www.googleapis.com/auth/youtube']
scopes = ['https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service(game):
    # flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    # credentials = flow.run_console()
    # return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    flow = flow_from_clientsecrets(settings.RESULT_DIRECTORY + game['client_secrets_file'],
                                   scopes,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage(settings.RESULT_DIRECTORY + game['credentials'])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        args = argparser.parse_args()
        args.noauth_local_webserver = True
        credentials = run_flow(flow, storage, args)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 http=credentials.authorize(httplib2.Http()))


def initialize_upload(youtube, file_path, title, description, category, tags, language):
    body = dict(
        snippet=dict(
            title=title,
            description=description,
            tags=tags,
            categoryId=category,
            defaultLanguage=language,
            defaultAudioLanguage=language
        ),
        status=dict(
            privacyStatus="public"
        )
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file_path, chunksize=1024*1024, resumable=True)
    )

    video_id = resumable_upload(insert_request)
    return video_id

# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            logging.info("Uploading file...")
            status, response = insert_request.next_chunk()
            if 'id' in response:
                logging.info("Video id '%s' was successfully uploaded." %
                      response['id'])
                return response['id']      
            else:
                exit("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                     e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

        except Exception as e:
            if error is not None:
                logging.error(e)

        if error is not None:
            logging.error(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            logging.info("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)


def upload_video(game, title, file_path, description, category, tags, fallback_title):
    logging.info('Starting youtube auth service')
    youtube = get_authenticated_service(game)
    language = game['language']
    try:
        logging.info('Starting upload process')
        video_id = initialize_upload(youtube, file_path, title,
                          description, category, tags, language)
        logging.info('video uploaded')
        return video_id
    except HttpError as e:
        logging.error("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
        if str(e.content).find('invalidTitle'):
            video_id = initialize_upload(youtube, file_path, fallback_title,
                          description, category, tags, language)
            logging.info('video uploaded with fallback title')
            return video_id


def upload_thumbnail(game, video_id, file):
    try:
        youtube = get_authenticated_service(game)
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=file
        ).execute()
        logging.info('Thumbnail uploaded')
    except HttpError as e:
        logging.warning("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

def get_video_thumbnail(video_id):
    thumbnails_game_credentials = game_config.GAMES['ark_es'] #chatting_es credentials are the ones with read videos scope access
    try:
        youtube = get_authenticated_service(thumbnails_game_credentials)
        request = youtube.videos().list(part="snippet", id=video_id
        )
        response = request.execute()
        thumbnail_url = response['items'][0]['snippet']['thumbnails']['maxres']['url']
        return thumbnail_url
    except HttpError as e:
        logging.warning("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    
