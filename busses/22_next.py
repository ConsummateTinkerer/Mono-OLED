#!/usr/bin/env python3

# General
import os
import time

# For the scraping
from bs4 import BeautifulSoup
import requests

# For the oled
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from threading import Thread
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

# Set up OLED
oled = sh1106(i2c(port=1, address=0x3C), rotate=2, height=128, width=128)

# Load fonts
rr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto_Regular.ttf'))
rb_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto_Black.ttf'))
rr_12 = ImageFont.truetype(rr_path, 12)
rr_24 = ImageFont.truetype(rr_path, 24)

# The main loop that writes to the OLED
while True:
	# Page url to scrape
	url ='https://www.buses.co.uk/stops/149000006645'

	# Fetch the content from url
	page = requests.get(url, timeout=5)

	# Parse html
	soup = BeautifulSoup(page.content, "html.parser")

	# Extract the html element where the next time expected is stored
	time_expected = soup.find(class_='single-visit__time--expected')

	# Strip extraneous html
	next_bus = time_expected.text.strip()

	# Start to draw to the display
	background = Image.open("/home/foo/Dev/Raspi/busses/images/bus.png").convert(oled.mode)
	draw = ImageDraw.ImageDraw(background)

	# Draw the top line
	draw.rectangle([(0, 0), (128, 20)], fill="black")
	draw.line([(0, 20), (128, 20)], fill="white")

	# Draw the text
	draw.rectangle([(0, 108), (128, 128)], fill="black")
	draw.text((10, 40), "The next bus is in", fill="white", font=rr_12)
	draw.text((20, 60), next_bus, fill="white", font=rr_24)

	# Draw the bottom line
	draw.rectangle([(0, 108), (128, 128)], fill="black")
	draw.line([(0, 108), (128, 108)], fill="white")

	# Display on the OLED
	oled.display(background)
	time.sleep(0.05)

