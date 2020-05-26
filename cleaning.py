import os
import logging
import settings

def clean_files():
    try:
        os.remove('result.mp4')
    except Exception as e:
        logging.info(str(e))
        pass
    for file in os.listdir(settings.DOWNLOADS_DIRECTORY):
        try:
            os.remove(os.path.join(settings.DOWNLOADS_DIRECTORY, file))
        except Exception as e:
            logging.info(str(e))
            pass
