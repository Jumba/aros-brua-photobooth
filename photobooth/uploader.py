import asyncio
import os
import subprocess
from enum import Enum
from os import path
from threading import Thread

import time

from photobooth import PRIVATE_KEY, REMOTE_NEW_IMAGES, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD


class Target(Enum):
    SERVER = 0
    INSTAGRAM = 1


class TransferStatus(Enum):
    SCHEDULED = 0
    IN_PROGRESS = 1
    COMPLETED = 2


class UploadManager(Thread):

    def __init__(self, app, upload_dir, uploaded_dir):
        super(UploadManager, self).__init__()
        self.app = app
        self.upload_dir = upload_dir
        self.uploaded_dir = uploaded_dir

        self.transfer_queue = set()
        self.transfer_status = {}
        self.canceled = False

    def abort(self):
        self.canceled = True

    def tag_files_for_upload(self):
        with self.app.transfer_lock:
            for file in os.listdir(self.upload_dir):
                filename = path.join(self.upload_dir, file)
                if path.isfile(filename) and not file == ".gitignore" and filename not in self.transfer_status:
                    # It's a set so it'll take care of duplicates if they should occur (they shouldn't)
                    print("{} scheduled for upload".format(filename))
                    self.transfer_queue.add(filename)
                    self.transfer_status[filename] = TransferStatus.SCHEDULED

    def upload(self, filename, target):
        if target.SERVER:
            subprocess.call('scp -i {} "{}" {}'.format(PRIVATE_KEY, filename, REMOTE_NEW_IMAGES), shell=True)
        elif target.INSTAGRAM:
            # Set, forget, and hope for the best.
            subprocess.Popen(["php", "-f", "photobooth/instagram_upload.php", filename, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD])



    def run(self):
        while True and not self.canceled:
            self.tag_files_for_upload()
            for filename in list(self.transfer_queue):
                self.transfer_status[filename] = TransferStatus.IN_PROGRESS
                if "main" in filename:
                    self.upload(filename, Target.INSTAGRAM)

                self.upload(filename, Target.SERVER)
                self.transfer_queue.remove(filename)
                self.transfer_status[filename] = TransferStatus.COMPLETED

            time.sleep(1)


