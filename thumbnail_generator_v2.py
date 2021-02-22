from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import settings
import requests
import random
import os

def generate_thumbnail(game, number, thumbnail_url):
    
    number_x = 820
    number_y = 50
    emoji_x = 100
    emoji_y = 370
    
    CMY = [(255,255,0), (255,0,255), (0,255,255)]

    thumbnail_image = Image.open(requests.get(thumbnail_url, stream=True).raw).convert('RGBA')
    
    numbers_directory = settings.UTILS_DIRECTORY
    number = str(number)

    hashtag_image = Image.open(
        numbers_directory + 'hashtag.png')
    thumbnail_image.paste(hashtag_image, (number_x, number_y), hashtag_image)
    
    for index, digit in enumerate(number):
        number_image = Image.open(numbers_directory + digit + '.png')
        thumbnail_image.paste(number_image, ((index+1)*90+number_x, number_y), number_image)
    
    emoji_path = random.choice(os.listdir(settings.UTILS_DIRECTORY + 'emojis/'))
    emoji_image = Image.open(settings.UTILS_DIRECTORY + 'emojis/' + emoji_path).convert('RGBA')
    emoji_image = emoji_image.resize((300, 300))
    thumbnail_image.paste(emoji_image, (emoji_x,emoji_y), emoji_image)

    random_color = random.choice(CMY)
    band_width = 36
    for x in range(0, band_width):
        for y in range(0, 720):
            thumbnail_image.putpixel((x,y), random_color)
    for x in range(1280-band_width, 1280):
        for y in range(0, 720):
            thumbnail_image.putpixel((x,y), random_color)
    for x in range(0, 1280):
        for y in range(0, 36):
            thumbnail_image.putpixel((x,y), random_color)
    for x in range(0, 1280):
        for y in range(720-band_width, 720):
            thumbnail_image.putpixel((x,y), random_color)                            

    thumbnail_image.save(settings.DOWNLOADS_DIRECTORY + 'thumbnail.png', "PNG")