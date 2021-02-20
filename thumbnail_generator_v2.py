from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import settings

def generate_thumbnail(game, number):
    x = game['thumbnail_number_x']
    y = game['thumbnail_number_y']
    
    img = Image.open(game['thumbnail_file'])
    numbers_directory = settings.UTILS_DIRECTORY
    number = str(number)

    
    hashtag_image = Image.open(
        numbers_directory + 'hashtag.png')
    img.paste(hashtag_image, (x, y), hashtag_image)
    
    for index, digit in enumerate(number):
        number_image = Image.open(numbers_directory + digit + '.png')
        img.paste(number_image, ((index+1)*90+x, y), number_image)
    


    img.save(settings.DOWNLOADS_DIRECTORY + 'thumbnail.png', "PNG")