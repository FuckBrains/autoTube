import os
import logging

def clean_files():
    try:
        os.remove('result.mp4')
    except Exception as e:
        logging.info(str(e))
        pass
    basepath = 'downloads/'
    for file in os.listdir(basepath):
        try:
            os.remove(os.path.join(basepath, file))
        except Exception as e:
            logging.info(str(e))
            pass
