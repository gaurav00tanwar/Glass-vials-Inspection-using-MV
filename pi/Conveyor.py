# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/
import time

import RPi.GPIO as GPIO
from time import sleep
import logging

logging.basicConfig(level='INFO')
log = logging.getLogger('Conveyor')


class Conveyor:
    __instance = None

    @staticmethod
    def get_instance():
        if Conveyor.__instance is None:
            return Conveyor()
        log.info("Fetching Conveyor instance")
        return Conveyor.get_instance()

    def __init__(self):
        if Conveyor.__instance is not None:
            log.info("Conveyor instance is not None")
        else:
            self.in1 = 24
            self.in2 = 23
            self.en = 25
            self.temp1 = 1
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.in1, GPIO.OUT)
            GPIO.setup(self.in2, GPIO.OUT)
            GPIO.setup(self.en, GPIO.OUT)
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.LOW)
            self.p = GPIO.PWM(self.en, 1000)
            self.p.start(30)

    def start_conveyor(self):
        log.info("Running Conveyor...")
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)

    def stop_conveyor(self):
        log.info("Stopping Conveyor...")
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()
        print("GPIO Clean up")

# if __name__ == "__main__":
#     conveyor = Conveyor.get_instance()
#     conveyor.start_conveyor()
#     time.sleep(10)
#     conveyor.stop_conveyor()
#     conveyor.cleanup()
