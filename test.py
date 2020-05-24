from PIL import Image, ImageDraw, ImageFont
from random import randint as rint
import os
import random
import settings
import textwrap


def generate_gradient():
    img = Image.new("RGB", (1280, 720), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    r, g, b = rint(0, 255), rint(0, 255), rint(0, 255)
    dr = (rint(0, 255) - r)/1280.
    dg = (rint(0, 255) - g)/1280.
    db = (rint(0, 255) - b)/1280.
    for i in range(1280):
        r, g, b = r+dr, g+dg, b+db
        draw.line((i, 0, i, 1280), fill=(int(r), int(g), int(b)))

    # img.save(name+".png", "PNG")
    return img


def add_effect(img):
    random_effect_path = random.choice(
        os.listdir(settings.THUMBNAIL_EFFECTS_DIRECTORY))
    effect = Image.open(
        settings.THUMBNAIL_EFFECTS_DIRECTORY + random_effect_path)
    img.paste(effect, (0, 0), effect)
    return img


def add_streamer(img):
    streamer_img = Image.open('tfue.png')
    bounding_box = streamer_img.getbbox()
    streamer_img = streamer_img.crop(bounding_box)
    streamer_img = streamer_img.resize((1280, 720))

    if random.choice([-1, 1]) == 1:
        streamer_img = streamer_img.transpose(Image.FLIP_LEFT_RIGHT)

    movement = 300 * random.choice([-1, 1])

    img.paste(streamer_img, (movement, 0), streamer_img)
    return img


def add_text(img):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Anton-Regular.ttf", 100)

    text = "SAMPLE TEXT!"

    wrapped_text = textwrap.wrap(text, width=5)


    current_h, pad = 30, 10
    for line in wrapped_text:
        w, h = draw.textsize(line, font=font)
        draw.text((200, current_h), line, font=font)
        current_h += h + pad

    # draw.text((0, 0), "SAMPLE TEXT!", (0, 0, 0), font=font)
    # draw.text((10, 10), "SAMPLE\n TEXT!", (255, 255, 255), font=font)
    return img


img = generate_gradient()
img = add_effect(img)
img = add_streamer(img)
img = add_text(img)
img.save('thumbnail.png', "PNG")
