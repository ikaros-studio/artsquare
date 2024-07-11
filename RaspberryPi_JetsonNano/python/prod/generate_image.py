#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import subprocess
import logging
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
    
from waveshare_epd import epd7in5_V2
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

def generate_image(prompt, output_path):
    try:
        # Adjust the command to match your OnnxStream setup
        subprocess.run([
            './sd',  # Path to the OnnxStream executable
            '--turbo',
            '--models-path', '/home/pi/stable-diffusion-models/stable-diffusion-xl-turbo-1.0-onnxstream',
            '--prompt', prompt,
            '--steps', '1',
            '--output', output_path,
            '--rpi'
        ], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to generate image: {e}")
        return False
    return True

try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    logging.info("Displaying generating message")
    # Create a blank image for the message
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    font = ImageFont.load_default()
    text = "Generating..."
    text_width, text_height = draw.textsize(text, font)
    draw.text(((epd.width - text_width) // 2, (epd.height - text_height) // 2), text, font=font, fill=0)
    epd.display(epd.getbuffer(Himage))

    # Generate the image
    prompt = "a beautiful scenery with mountains and a river"
    output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../assets/img/generated_image.png')
    if generate_image(prompt, output_path):
        logging.info("Displaying generated image")
        Himage = Image.open(output_path)
        Himage = Himage.convert('1')
        Himage = Himage.resize((epd.width, epd.height), Image.ANTIALIAS)  # Resize to fit the display
        epd.display(epd.getbuffer(Himage))
    else:
        logging.error("Failed to generate image")

    time.sleep(2)

    logging.info("Clear...")
    epd.init()
    epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.error(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()
