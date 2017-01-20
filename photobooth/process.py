import os
import shutil
from os.path import isfile, join
from threading import Thread
from uuid import uuid4

from photobooth.render import create_collage


class ThreadedMover(Thread):
    def __init__(self, processor, batch_code):
        super(ThreadedMover, self).__init__()
        self.processor = processor
        self.batch_code = batch_code

    def run(self):
        for file in os.listdir(self.processor.in_dir):
            filename = join(self.processor.in_dir, file)
            if isfile(filename) and self.batch_code in file:
                shutil.move(filename, join(self.processor.out_dir, self.processor.get_filename()))


class ImageProcessor(object):
    def __init__(self, app, options, in_dir, out_dir):
        self.app = app
        self.options = options
        self.in_dir = in_dir
        self.out_dir = out_dir

    def on_collage_complete(self, image):
        filename = self.get_filename()
        image.save(join(self.out_dir, 'main-{}'.format(filename)))
        t = ThreadedMover(self, self.app.camera.get_batch_code())
        t.start()

        self.app.next_image(filename)

    def process(self):
        self.app.clear_next()
        files = []
        for file in os.listdir(self.in_dir):
            if isfile(join(self.in_dir, file)):
                files.append(join(self.in_dir, file))

        # Single shot
        if len(files) == 1:
            filename = self.get_filename()
            shutil.move(files[0], join(self.out_dir, 'main-{}'.format(filename)))
            self.app.next_image(filename)
        elif len(files) > 1:
            # Create a collage.
            print("collage_Start")
            create_collage(files, self.options, self.on_collage_complete)

    def get_filename(self):
        return "{}.jpg".format(str(uuid4()))
