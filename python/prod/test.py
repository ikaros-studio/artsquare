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
import argparse
import datetime

logging.basicConfig(level=logging.DEBUG)

def parse_arguments():
    parser = argparse.ArgumentParser(description='E-Ink Frame Power Management')
    parser.add_argument('--interval', type=int, default=3600, help='Interval in seconds between image generations')
    return parser.parse_args()

args = parse_arguments()

onnxstream_executable = '/home/pi/OnnxStream/src/build/sd'
last_run_file = '/home/pi/artframe/last_run.txt'

def generate_image(prompt, output_path):
    logging.debug(f"Checking if OnnxStream executable exists at {onnxstream_executable}")
    if not os.path.exists(onnxstream_executable):
        logging.error(f"OnnxStream executable not found: {onnxstream_executable}")
        return False

    logging.debug(f"Checking execute permissions for {onnxstream_executable}")
    if not os.access(onnxstream_executable, os.X_OK):
        logging.info(f"Setting execute permissions for: {onnxstream_executable}")
        try:
            os.chmod(onnxstream_executable, 0o755)
        except Exception as e:
            logging.error(f"Failed to set execute permissions: {e}")
            return False

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

def power_off_system():
    logging.info("Shutting down the system to conserve power.")
    os.system("sudo shutdown now")

def schedule_wakeup():
    logging.info("Scheduling system wakeup")
    # This schedules the wakeup in args.interval seconds
    os.system(f"sudo rtcwake -m no -s {args.interval}")

def check_power_interruption(last_run_file):
    if not os.path.exists(last_run_file):
        return True

    with open(last_run_file, 'r') as file:
        last_run = datetime.datetime.fromisoformat(file.read().strip())

    now = datetime.datetime.now()
    if (now - last_run).total_seconds() > args.interval:
        return True
    return False

def update_last_run_time(last_run_file):
    with open(last_run_file, 'w') as file:
        file.write(datetime.datetime.now().isoformat())

try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()

    logging.info("Init and Clear")
    epd.init()
    epd.Clear()

    if check_power_interruption(last_run_file):
        logging.info("Displaying generating message")
        Himage = Image.new('1', (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(Himage)
        font = ImageFont.load_default()
        text = "Generating something ..."
        text_width, text_height = draw.textsize(text, font)
        draw.text(((epd.width - text_width) // 2, (epd.height - text_height) // 2), text, font=font, fill=0)
        epd.display(epd.getbuffer(Himage))

        logging.info("Putting display to sleep during image generation")
        epd.sleep()

        prompt = "A beautiful sunset over the mountains."
        output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../assets/img/generated_image.png')

        logging.info(f"Starting image generation with prompt: {prompt}")
        logging.info(f"Output path for generated image: {output_path}")

        logging.info("Waking up the display")
        epd.init()

        if generate_image(prompt, output_path):
            logging.info("Displaying generated image")
            Himage = Image.open(output_path)
            Himage = Himage.convert('1')
            Himage = Himage.resize((epd.width, epd.height), Image.ANTIALIAS)
            epd.display(epd.getbuffer(Himage))
            update_last_run_time(last_run_file)
        else:
            logging.error("Failed to generate image")

        time.sleep(2)

        logging.info("Clear...")
        epd.init()

        logging.info("Goto Sleep...")
        epd.sleep()

        schedule_wakeup()
        power_off_system()
    else:
        logging.info("No power interruption detected. Waiting for the next scheduled run.")

except IOError as e:
    epd.sleep()
    logging.error(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd.sleep()
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()
