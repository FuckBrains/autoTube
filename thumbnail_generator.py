from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from random import randint as rint
import google_images_download_fork
import os
import random
import settings
import textwrap
import requests
import logging


def download_from_google(streamer_name):
    downloader = google_images_download_fork.googleimagesdownload()

    # Format must be png and limit must be 1 since chuski1212 has modified the forked downloader, otherwise it will fail
    arguments = {"keywords": streamer_name +
                 ' face streamer', "limit": 1, "print_urls": True, "output_directory": settings.DOWNLOADS_DIRECTORY,
                  "no_directory": True, "prefix": streamer_name, "format": "png"}
    
    paths = downloader.download(arguments)
    print(paths)


def remove_bg(file_path):
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(file_path, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': settings.REMOVE_BG_KEY},
    )
    if response.status_code == requests.codes.ok:
        with open(file_path, 'wb') as out:
            out.write(response.content)
        logging.info('Remove bg API used')    
    else:
        print("Error:", response.status_code, response.text)
        raise ResourceWarning(str(response.text))

def generate_gradient(width, height):
    img = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    r, g, b = rint(0, 255), rint(0, 255), rint(0, 255)
    dr = (rint(0, 255) - r)/width
    dg = (rint(0, 255) - g)/width
    db = (rint(0, 255) - b)/width
    for i in range(width):
        r, g, b = r+dr, g+dg, b+db
        draw.line((i, 0, i, width), fill=(int(r), int(g), int(b)))

    # img.save(name+".png", "PNG")
    return img


def add_effect(img):
    random_effect_path = random.choice(
        os.listdir(settings.THUMBNAIL_EFFECTS_DIRECTORY))
    effect = Image.open(
        settings.THUMBNAIL_EFFECTS_DIRECTORY + random_effect_path)
    img.paste(effect, (0, 0), effect)
    return img


def add_streamer(img, side, streamer_name):
    streamer_img = Image.open(settings.DOWNLOADS_DIRECTORY + streamer_name + '.png')
    bounding_box = streamer_img.getbbox()
    streamer_img = streamer_img.crop(bounding_box)
    streamer_img = streamer_img.resize((1280, 720))

    if random.choice([True, False]):
        streamer_img = streamer_img.transpose(Image.FLIP_LEFT_RIGHT)

    movement = 300 * side

    img.paste(streamer_img, (movement, 0), streamer_img)
    return img


def add_text(img, side, text):
    
    front_text = Image.new('RGBA', (1280, 720))
    draw = ImageDraw.Draw(front_text)
    
    font = ImageFont.truetype("buchanan.ttf", 160)

    splitted = text.split(' ')
    letters = 0
    text = ''
    for word in splitted:
        text += word
        letters += len(word)
        if letters >= 6:
            text += '\n'
            letters = 0
        else:
            text += ' '
    draw.text((0, 0), text, (255, 255, 255), font=font)

    bbox = front_text.getbbox()
    front_text = front_text.crop(bbox)

    r, g, b, a = front_text.split()
    rgb_image = Image.merge('RGB', (r, g, b))
    inverted_image = ImageOps.invert(rgb_image)
    r2, g2, b2 = inverted_image.split()
    inverted_image = Image.merge('RGBA', (r2, g2, b2, a))

    bbox = front_text.getbbox()
    front_text = front_text.crop(bbox)

    shadow = inverted_image.filter(ImageFilter.GaussianBlur(radius=6))

    bbox = shadow.getbbox()
    shadow = shadow.crop(bbox)

    gradient = generate_gradient(bbox[2], bbox[3])
    width, height = front_text.size
    for i in range(width):
        for j in range(height):
            pixel = front_text.getpixel((i, j))
            if pixel == (255, 255, 255, 255):
                front_text.putpixel((i, j), gradient.getpixel((i, j)))

    img.paste(shadow, (240 + 150 * side * -1, 100), shadow)
    img.paste(shadow, (260 + 150 * side * -1, 100), shadow)
    img.paste(shadow, (250 + 150 * side * -1, 90), shadow)
    img.paste(shadow, (250 + 150 * side * -1, 110), shadow)
    img.paste(shadow, (240 + 150 * side * -1, 90), shadow)
    img.paste(shadow, (240 + 150 * side * -1, 110), shadow)
    img.paste(shadow, (260 + 150 * side * -1, 90), shadow)
    img.paste(shadow, (260 + 150 * side * -1, 110), shadow)
    img.paste(front_text, (250 + 150 * side * -1, 100), front_text)
    return img

def get_streamer_image(streamer_name):
    streamer_image_path = settings.DOWNLOADS_DIRECTORY + streamer_name + '.png'
    if os.path.exists(streamer_image_path):
        pass
    else:
        download_from_google(streamer_name)
        remove_bg(streamer_image_path)



def generate_thumbnail(streamer_name, title):
    get_streamer_image(streamer_name)
    img = generate_gradient(1280, 720)
    img = add_effect(img)
    side = random.choice([-1, 1])
    img = add_streamer(img, side, streamer_name)
    img = add_text(img, side, title)
    img.save(settings.DOWNLOADS_DIRECTORY + 'thumbnail.png', "PNG")
