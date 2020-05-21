import os


def clean_files():
    try:
        os.remove('result.mp4')
    except:
        pass
    basepath = 'downloads/'
    for file in os.listdir(basepath):
        os.remove(os.path.join(basepath, file))
