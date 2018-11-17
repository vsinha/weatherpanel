from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import forecastio
import time
import os

import font_utils
import raspi_utils
import Frame

dirname = os.path.dirname(__file__)
roboto_black = os.path.join(dirname, 'fonts/RobotoMono-Bold.ttf')
roboto_bold = os.path.join(dirname, 'fonts/Roboto-Bold.ttf')
darksky_file = os.path.join(dirname, 'darksky_key')

bigfont = ImageFont.truetype(roboto_black, 200)
smallfont = ImageFont.truetype(roboto_bold, 20)

width = 640
halfwidth = width / 2
height = 384
halfheight = height / 2

lat = 40.688727
lng = -73.982624

test_raspi = False
if raspi_utils.is_raspberry_pi() or test_raspi:
    image_mode = 1
    white = 255
else:    
    image_mode = "RGB"
    white = (255, 255, 255)


def load_darksky_api_key():
    with open(darksky_file) as f:
        return f.readline()

darksky_key = load_darksky_api_key()


def get_time():
    time.ctime() # 'Mon Oct 18 13:35:29 2010'
    return time.strftime('%l:%M%p %Z on %b %d, %Y') # ' 1:36PM EDT on Oct 18, 2010'


def update():
    update_time = get_time()

    forecast = forecastio.load_forecast(darksky_key, lat, lng)

    image = Image.new(image_mode, (width, height), white)    # 1: clear the frame
    draw = ImageDraw.Draw(image)

    left_half_rect = ((0,0), (int(width / 2), height))
    draw.rectangle(left_half_rect, fill=0)
    draw_temp(draw, forecast, roboto_black, left_half_rect)

    right_half_rect = ((int(width / 2), height), (width, height))
    draw_summary(draw, forecast, roboto_bold, right_half_rect)

    font_utils.draw_text_in_frame(draw, update_time, roboto_bold, ((halfwidth, height - 30), (width, height)), 0)

    return image


def draw_temp(draw, forecast, fontpath, framesize):
    temp = forecast.currently().apparentTemperature
    text = str(int(round(temp, 0)))
    font_utils.draw_text_in_frame(draw, text, roboto_black, framesize, white)



def draw_summary(draw, forecast, fontpath, frame):
    text = forecast.hourly().summary
    font = ImageFont.truetype(fontpath, 30)
    width = Frame.width(frame)
    
    wrapped = font_utils.wrap_text_to_width(text, font, width - 20)
    size = draw.textsize(wrapped, font)

    draw.text((halfwidth + 10, halfheight - (size[1] / 2)), wrapped, font = font, fill = 0)


def main():
    image = update()

    if raspi_utils.is_raspberry_pi():
        raspi_utils.send_to_eink(image)
    else:
        filename = "output.jpg"
        image.save(filename)


if __name__ == '__main__':
    main()
