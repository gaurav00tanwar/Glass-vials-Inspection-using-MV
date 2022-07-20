import logging
import threading
import time

from Camera import Camera
from flask_server import send_captured_image
import os

logging.basicConfig(level='INFO')
log = logging.getLogger("MAIN")


class Main:
    __instance = None

    @staticmethod
    def get_instance():
        if Main.__instance is None:
            return Main()
        log.info("Fetching Main Instance")
        return Main.__instance

    def __init__(self):
        if Main.__instance is not None:
            log.info("Main instance is not None")
        else:
            self.dirPath = '/home/gaurav/Desktop/gphoto/images/'
            self.camera = Camera.get_instance()

    def run(self):
        t = threading.Thread(target=self.run_loop)
        t.daemon = True
        t.start()

    def run_loop(self):
        file_name = self.camera.run()
        log.info("File Name: ", file_name)
        file = os.open(self.dirPath + file_name, os.O_RDWR)
        send_captured_image(file)
        log.info("Sleeping")
        time.sleep(20)
        log.info("Sleep Over")


# if __name__ == "__main__":
#     main_loop = Main.get_instance()
#     main_loop.run()
