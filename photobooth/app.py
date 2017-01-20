from threading import Lock

import sys
from qtpy.QtWidgets import QApplication

from photobooth import NEW_IMAGES, Options, PROCESSED_IMAGES
from photobooth.camera import Camera
from photobooth.process import ImageProcessor


class PhotoboothApplication(QApplication):

    def __init__(self, *argv):
        QApplication.__init__(self, *argv)

        self.transfer_lock = Lock()
        self.setup = False
        self.camera = None
        self.options = Options()
        self.processor = ImageProcessor(self, self.options, NEW_IMAGES, PROCESSED_IMAGES)

        self._next_image = None

    def setup_photobooth(self, camera_model):
        self.camera = Camera(self, camera_model, NEW_IMAGES)
        self.setup = True

    def start(self):
        assert self.setup, "Setup not completed.'"

    def exit(self, message):
        print("Exiting: {}".format(message))
        sys.exit(0)

    def next_image(self, filename):
        self._next_image = filename

    def clear_next(self):
        self._next_image = None

    def single_shot(self):
        self.camera.take_picture()
        self.camera.download_images()
        self.processor.process()

    def collage_shot(self):
        self.camera.take_picture(count=4, interval=1)
        self.camera.download_images()
        self.processor.process()
