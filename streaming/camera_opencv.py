import os
import sys
PYTHON_PATH = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(PYTHON_PATH, '..')))
import cv2
from base_camera import BaseCamera
import requests
import base64
import json

from streaming.read_info import camera_source, api


class Camera(BaseCamera):
    video_source = camera_source

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        # from run import api
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        frame_count = 0
        id2class = {0: 'lp'}
        color = (255, 0, 0)
        
        while True:
            # read current frame
            _, img = camera.read()

            frame_count += 1
            if frame_count % 3 != 0:
                continue
            
            _, buff = cv2.imencode('.jpg', img)
            jpg_as_text = base64.b64encode(buff)

            payload = {'image': jpg_as_text}
            response = requests.post(api, data=payload)
            
            if response.status_code != 200:
                continue
            lps_res = response.json()


            # Draw bounding box
            for idx, data in lps_res.items():
                tl = (int(data['tl'][0]), int(data['tl'][1]))
                br = (int(data['br'][0]), int(data['br'][1]))
                conf = data['conf']
                cls = data['cls']
                cv2.rectangle(img, tl, br, color, 2)
                cv2.putText(img, 
                            "%s: %.2f" % (id2class[cls], conf), 
                            (tl[0] + 2, tl[1] - 2),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, 
                            color)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
