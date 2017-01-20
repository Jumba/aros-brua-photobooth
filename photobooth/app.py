import signal
from threading import Lock

import sys
from qtpy.QtWidgets import QApplication, QMainWindow, QLabel
import qtpy.QtGui as QtGui

from photobooth import NEW_IMAGES, Options, PROCESSED_IMAGES, UPLOADED_IMAGES
from photobooth.camera import Camera
from photobooth.process import ImageProcessor
from photobooth.serial import SerialListener
from photobooth.uploader import UploadManager


class PhotoboothApplication(QApplication):

    def __init__(self, *argv):
        QApplication.__init__(self, *argv)

        self.transfer_lock = Lock()
        self.setup = False
        self.camera = None
        self.image_window = None
        self.options = Options()
        self.processor = ImageProcessor(self, self.options, NEW_IMAGES, PROCESSED_IMAGES)
        self.uploader = UploadManager(self, PROCESSED_IMAGES, UPLOADED_IMAGES )
        self.listener = SerialListener(self)
        self.listener.left.connect(self.left_button)
        self.listener.right.connect(self.right_button)
        self.listener.start()

        self._next_image = None

    def setup_photobooth(self, camera_model):
        self.camera = Camera(self, camera_model, NEW_IMAGES)
        self.setup = True
        self.uploader.start()

    def start(self):
        assert self.setup, "Setup not completed.'"

    def force_exit(self, message):
        print("Exiting: {}".format(message))
        sys.exit(0)

    def next_image(self, filename):
        self._next_image = filename
        self.image_window = PhotoWindow(self, filename, None)
        self.image_window.show()

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

    def left_button(self):
        print("left")
        self.next_image('/home/calvin/Documents/Develop/aros-brua-photobooth/out/new_images/28748c7b-72aa-4de9-804c-84d061b4c9c6.jpg')

    def right_button(self):
        print("right")
        if self.image_window:
            self.image_window.hide()




class PhotoWindow(QMainWindow):

    def __init__(self, app, filename, flags, *args, **kwargs):
        super(PhotoWindow, self).__init__(flags, *args, **kwargs)
        self.app = app
        self.filename = filename

        self.init()

    def init(self):
        self.setGeometry(0, 0, 1500, 1000)
        pic = QLabel(self)
        pic.setGeometry(0,0, 1500, 1000)
        pixmap = QtGui.QPixmap(self.filename)
        pixmap = pixmap.scaledToHeight(1000)
        pic.setPixmap(pixmap)
        self.center()

    def center(self):
        frame_gm = self.frameGeometry()
        screen =  self.app.desktop().screenNumber( self.app.desktop().cursor().pos())
        center_point = self.app.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())