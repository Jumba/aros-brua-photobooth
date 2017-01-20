# Where to spit out our qrcode, watermarked image, and local html
import os
from os.path import expanduser, join

current_directory = os.getcwd()

NEW_IMAGES = join(current_directory, 'out', 'new_images')
PROCESSED_IMAGES = join(current_directory, 'out', 'processed_images')
UPLOADED_IMAGES = join(current_directory, 'out', 'uploaded_images')

# The watermark to apply to all images
WATERMARK = join(current_directory, 'resources', 'brua-school-2.png')

REMOTE_NEW_IMAGES = 'root@178.62.225.50:/var/www/raw'
PRIVATE_KEY = expanduser('~/.ssh/id_rsa')

HTTP_SERVE_URL = 'http://arosbrua.nl:8000/raw/'

# Size of the qrcode pixels
QR_CODE_SIZE = 10

QUALITY_SKEL = 0
QUALITY_FAST = 1
QUALITY_BEST = 2


class Options(object):
    def __init__(self):
        self.border_w = 0.01
        self.border_c = "black"
        self.out_w = 3888
        self.out_h = 2592
        self.multi_col = False
