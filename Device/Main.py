import logging
import threading
from CrackDetection import CrackDetection
import os
logging.basicConfig(level='INFO')
log = logging.getLogger("MAIN")


class Main:
    __instance = None

    @staticmethod
    def get_instance(self):
        if Main.__instance is None:
            return Main()
        log.info("Fetching Main Instance")
        return Main.__instance

    def __init__(self):
        if Main.__instance is not None:
            log.info("Main instance is not None")
        else:
            self.dirPath = '/home/gaurav/Desktop/gphoto/images/'
            self.crack_detection = CrackDetection.get_instance()

    def run(self):
        t = threading.Thread(target=self.run_loop)
        t.daemon = True
        t.start()

    def run_loop(self):
        file_name = self.crack_detection.detect_function()
        log.info("File Name: ", file_name)
