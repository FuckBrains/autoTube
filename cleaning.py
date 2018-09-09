import os


def clean_files():
    os.remove('result.mp4')
    basepath = 'downloads/'
    for file in os.listdir(basepath):
        os.remove(os.path.join(basepath, file))
