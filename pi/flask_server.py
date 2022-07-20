from flask import Flask, request
import os
import logging
# from Camera import Camera
# from Main import Main
import requests
from threading import Thread

logging.basicConfig(level='INFO')
log = logging.getLogger("FLASK")

app = Flask(__name__)
# main_app = Main.get_instance()
# main_app.run()
#
# dir = "/home/gaurav/Desktop/gphoto/images/"


def send_captured_image(file):
    try:
        with open(file, "rb") as cam_file:
            log.info('Sending Captured Image')
            url = 'http://192.168.1.38:5000/crack'

            req = requests.post(url, files={'cam': cam_file})
            resp = req.json()
            log.info(resp)
    except Exception as e:
        log.warning(e)


# t1 = Thread(target=lambda: app.run(host='0.0.0.0', debug=False, threaded=True, use_reloader=False))
# t1.start()
