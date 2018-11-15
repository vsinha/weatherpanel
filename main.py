from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#import imagedata
import forecastio
import time

import epd7in5

bigfont = ImageFont.truetype('fonts/Roboto-Black.ttf', 100)
smallfont = ImageFont.truetype('fonts/Roboto-Bold.ttf', 20)

width = 640
height = 384

lat = 40.688727
lng = -73.982624

def load_darksky_api_key():
    with open("darksky_key") as f:
        return f.readline()

darksky_key = load_darksky_api_key()

def get_temp(forecast):
    temp = forecast.currently().apparentTemperature
    temp = int(round(temp, 0))

    return str(temp) + " F outside"

def get_time():
    time.ctime() # 'Mon Oct 18 13:35:29 2010'
    return time.strftime('%l:%M%p %Z on %b %d, %Y') # ' 1:36PM EDT on Oct 18, 2010'

def update():

    update_time = "updated: " + get_time()

    forecast = forecastio.load_forecast(darksky_key, lat, lng)
    temp_str = get_temp(forecast)
    summary_str = forecast.currently().summary

    image = Image.new('1', (width, height), 1)    # 1: clear the frame
    draw = ImageDraw.Draw(image)

    draw.text((50, 100), temp_str, font = bigfont, fill = 0)
    draw.text((50, 220), summary_str, font = smallfont, fill = 0)
    draw.text((50, 260), update_time, font = smallfont, fill = 0)

    image = image.rotate(180)
    image.show()

def main():
    # epd = epd7in5.EPD()
    # epd.init()

    update()


if __name__ == '__main__':
    main()
