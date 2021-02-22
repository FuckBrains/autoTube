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
    
    CMY = ["#FFFF00", "#FF00FF", "#00FFFF"]

    bg = Image.new("RGBA", (1280, 720), random.choice(CMY))
    thumbnail_image = Image.open(requests.get(thumbnail_url, stream=True).raw).convert('RGBA')
    thumbnail_image = thumbnail_image.resize((1152, 648))
    
    bg.paste(thumbnail_image, (64,36), thumbnail_image)
    
    numbers_directory = settings.UTILS_DIRECTORY
    number = str(number)

    hashtag_image = Image.open(
        numbers_directory + 'hashtag.png')
    bg.paste(hashtag_image, (number_x, number_y), hashtag_image)
    
    for index, digit in enumerate(number):
        number_image = Image.open(numbers_directory + digit + '.png')
        bg.paste(number_image, ((index+1)*90+number_x, number_y), number_image)
    
    emoji_path = random.choice(os.listdir(settings.UTILS_DIRECTORY + 'emojis/'))
    emoji_image = Image.open(settings.UTILS_DIRECTORY + 'emojis/' + emoji_path).convert('RGBA')
    emoji_image = emoji_image.resize((300, 300))
    bg.paste(emoji_image, (emoji_x,emoji_y), emoji_image)

    bg.save(settings.DOWNLOADS_DIRECTORY + 'thumbnail.png', "PNG")