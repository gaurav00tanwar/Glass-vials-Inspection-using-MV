import werkzeug.datastructures
from flask import Flask, request, send_from_directory
import logging
from CrackDetection import CrackDetection
from PIL import Image
import PIL
import time
import os
from threading import Thread

logging.basicConfig(level='INFO')
log = logging.getLogger('FLASK')

app = Flask(__name__)

# path_dir = "C:\Users\Prabhat Ranjan\Desktop\gphoto"

crack_detection = CrackDetection.get_instance()


@app.route('/crack', methods=['POST'])
def fetch_capture_image():
    request_files = request.files
    # content = request.content
    log.info(request_files['cam'])
    file = request_files['cam']
    if file:
        # filename = file.filename
        # print(filename)
        print(file)
        img = Image.open(file)
        print(img.size)
        img.save('output.jpg')
        # path = os.path.join('C:/Users/Prabhat Ranjan/Desktop/gphoto/img1.jpg')
        # im1 = Image.open(path)
        # im1.save(file)
        # f = open('C:/Users/Prabhat Ranjan/Desktop/gphoto/' + filename, mode='w')
        # f.write(file)
        crack_detection.detect_function('output.jpg')
    return {"Success": True}


#
# while True:
#     time.sleep(20)
t1 = Thread(target=lambda: app.run(host='0.0.0.0', debug=False, threaded=True, use_reloader=False))
t1.start()
