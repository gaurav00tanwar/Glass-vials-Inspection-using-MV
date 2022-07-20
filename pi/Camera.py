import logging
import time
from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess
import logging
from flask_server import send_captured_image
from Conveyor import Conveyor
logging.basicConfig(level='INFO')
log = logging.getLogger("CAMERA")


class Camera:
    __instance = None

    @staticmethod
    def get_instance():
        if Camera.__instance is None:
            return Camera()
        log.info("Fetching Camera Instance")
        return Camera.__instance

    def __init__(self):
        if Camera.__instance is not None:
            log.info("Camera Instance is not None")
            # raise Exception("Camera Instance is not None")
        else:
            self.shot_date = None
            self.shot_time = None,
            self.picID = 'PiShots'
            self.clearCommand = ["--folder", "/store_00020001/DCIM/100D3000/", "-R", "--delete-all-files"]
            self.triggerCommand = ["--trigger-capture"]
            self.downloadCommand = ["--get-all-files"]
            self.save_location = "/home/gaurav/Desktop/gphoto/images"

    def kill_gphoto2_process(self):
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            if b'gvfsd-gphoto2' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    # shot_date = datetime.now().strftime("%Y-%m-%d")
    # shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # picID = "PiShots"
    # clearCommand = ["--folder", "/store_00020001/DCIM/100D3000/", "-R", "--delete-all-files"]
    # triggerCommand = ["--trigger-capture"]
    # downloadCommand = ["--get-all-files"]
    # folder_name = shot_date + picID
    # save_location = "/home/gaurav/Desktop/gphoto/images" + folder_name

    def create_save_folder(self):
        try:
            os.makedirs(self.save_location)
        except OSError:
            log.info("Directory Already exists")
        except:
            log.info("Error Creating the directory")
        os.chdir(self.save_location)

    def capture_images(self):
        gp(self.triggerCommand)
        sleep(3)
        gp(self.downloadCommand)
        gp(self.clearCommand)

    def rename_files(self, ID):
        for filename in os.listdir("."):
            if len(filename) < 13:
                if filename.endswith(".JPG"):
                    os.rename(filename, (self.shot_time + ID + ".JPG"))
                    log.info("Renamed the JPG")
                    return self.shot_time + ID + ".JPG"
                elif filename.endswith(".CR2"):
                    os.rename(filename, (self.shot_time + ID + ".CR2"))
                    log.info("Renamed the CR2")
                    return self.shot_time + ID + ".CR2"

    def run(self):
        self.kill_gphoto2_process()
        gp(self.clearCommand)
        self.create_save_folder()
        self.capture_images()
        self.shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file = self.rename_files(self.picID)
        # log.info(file)
        return file


# killgphoto2Process()
# gp(clearCommand)
# createSaveFolder()
# captureImages()
# renameFiles(picID)


if __name__ == "__main__":
    dirPath = '/home/gaurav/Desktop/gphoto/images/'
    conveyor = Conveyor.get_instance()
    camera = Camera.get_instance()
    while True:
        conveyor.start_conveyor()
        time.sleep(2)
        conveyor.stop_conveyor()
        file_name = camera.run()
        # file = os.open(dirPath + file_name, os.O_RDWR)
        send_captured_image(file_name)
        print("Sleeping")
        time.sleep(20)
        print("Sleep Over")
