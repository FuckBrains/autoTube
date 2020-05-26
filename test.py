from PIL import Image, ImageDraw, ImageFont, ImageFilter
from random import randint as rint
import os
import random
import settings
import textwrap


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
    transparent = Image.new('RGBA', (1280, 720), (255, 0, 0, 0))

    draw = ImageDraw.Draw(transparent)
    font = ImageFont.truetype("jhuf.ttf", 100)

    text = "SAMPLE TEXT!"

    # wrapped_text = textwrap.wrap(text, width=5)
    # current_h, pad = 30, 10
    # for line in wrapped_text:
    #     w, h = draw.textsize(line, font=font)
    #     draw.text((200, current_h), line, font=font)
    #     current_h += h + pad

    draw.text((0, 0), "SAMPLE TEXT!", (0, 0, 0), font=font)
    # draw.text((0, 0), "SAMPLE TEXT!", (255, 255, 255), font=font)

    bbox = transparent.getbbox()
    transparent = transparent.crop(bbox)
    gradient = generate_gradient(bbox[2], bbox[3])
    gradient.save('gradient.png', 'PNG')
    width, height = transparent.size
    # for i in range(width):
    #     for j in range(height):
    #         pixel = transparent.getpixel((i, j))
    #         if pixel == (255, 255, 255, 255):
    #             transparent.putpixel((i, j), gradient.getpixel((i, j)))
    transparent = transparent.filter(ImageFilter.GaussianBlur(radius=5))
    transparent.save('testing.png', 'PNG')  
    return img


img = generate_gradient(1280, 720)
img = add_effect(img)
img = add_streamer(img)
img = add_text(img)
img.save('thumbnail.png', "PNG")
