#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
import subprocess


logging.basicConfig(level=logging.DEBUG)

def generate_image(prompt, output_path):
    onnxstream_executable = '/home/pi/OnnxStream/src/build/sd'  # Path to the OnnxStream executable
    
    logging.debug(f"Checking if OnnxStream executable exists at {onnxstream_executable}")
    # Check if the OnnxStream executable exists
    if not os.path.exists(onnxstream_executable):
        logging.error(f"OnnxStream executable not found: {onnxstream_executable}")
        return False

    logging.debug(f"Checking execute permissions for {onnxstream_executable}")
    # Check if the file has execute permissions, if not, set them
    if not os.access(onnxstream_executable, os.X_OK):
        logging.info(f"Setting execute permissions for: {onnxstream_executable}")
        try:
            os.chmod(onnxstream_executable, 0o755)
        except Exception as e:
            logging.error(f"Failed to set execute permissions: {e}")
            return False

    # Get current working directory
    cwd = os.getcwd()
    logging.info(f"Current working directory: {cwd}")

    # Set environment variables
    env = os.environ.copy()

    logging.debug(f"Running OnnxStream with prompt: {prompt}")
    try:
        result = subprocess.run([
            onnxstream_executable,
            '--turbo',
            '--models-path', '/home/pi/stable-diffusion-models/stable-diffusion-xl-turbo-1.0-onnxstream',
            '--prompt', prompt,
            '--steps', '1',
            '--output', output_path,
            '--rpi'
        ], check=True, env=env, capture_output=True, text=True)
        logging.info(f"Subprocess output: {result.stdout}")
        logging.error(f"Subprocess stderr: {result.stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to generate image: {e}")
        logging.error(f"Error output: {e.stderr}")
        return False
    logging.info(f"Image generated successfully: {output_path}")
    return True

try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    
    logging.info("Init and Clear")
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
    
    logging.info(f"Starting image generation with prompt: {prompt}")
    logging.info(f"Output path for generated image: {output_path}")
    
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
    epd.sleep()
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()
