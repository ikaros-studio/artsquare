#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
from PIL import Image
import traceback

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Add the directory containing waveshare_epd to the Python path
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

try:
    from waveshare_epd import epd7in5_V2
except ImportError as e:
    logging.error("Could not import epd7in5_V2 module. Please make sure the waveshare_epd library is installed and accessible.")
    sys.exit(1)

try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    logging.info("read jpg file")
    # Define the path to the JPG image
    jpg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../assets/img/cat.jpg')
    Himage = Image.open(jpg_path)
    
    # Convert the image to 1-bit color
    Himage = Himage.convert('1')
    
    # Resize the image to fit the e-paper display
    Himage = Himage.resize((epd.width, epd.height), Image.ANTIALIAS)

    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    logging.info("Clear...")
    epd.init()
    epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()
