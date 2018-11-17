from PIL import ImageFont
import textwrap

import Frame

def scale_font_to_width(text, fontpath, target_width):
    fontsize = 1
    font = ImageFont.truetype(fontpath, fontsize)

    while font.getsize(text)[0] < target_width:
        fontsize += 1
        font = ImageFont.truetype(fontpath, fontsize)

    return font

    
def wrap_text_to_width(text, font, width):
    line_length = len(text) # start with all of it
    lines = [text]
    while font.getsize(lines[0])[0] >= width:
        line_length -= 1
        lines = textwrap.wrap(text, line_length)
    print(repr(lines))
    return "\n".join(lines)



def draw_text_in_frame(draw, text, fontpath, frame, color, margin_fraction=0.9):
    framewidth = Frame.width(frame)
    font = scale_font_to_width(text, fontpath, framewidth * margin_fraction)
    textsize = draw.textsize(text, font = font)

    offset = font.getoffset(text)
    text_x = (frame[0][0] + frame[1][0] - textsize[0] - offset[0]) / 2
    text_y = (frame[0][1] + frame[1][1] - textsize[1] - offset[1]) / 2 

    draw.text((text_x, text_y), text, font = font, fill = color)

    bounds = ((text_x + offset[0], text_y + offset[1]), (text_x + textsize[0], text_y + textsize[1]))
    # draw.rectangle(frame, outline="green")
    # draw.rectangle(bounds, outline="red")
    return bounds
