import os
import base64

import cv2
import requests
import gradio as gr

url = "http://172.16.8.39:8000/api/detector/lp"
id2class = {0: "lp"}
color = (255, 0, 0)

def predict(img):
    _, buff = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buff)

    payload = {'image': jpg_as_text}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        return img

    lps_res = response.json()

    # Draw bounding box
    for idx, data in lps_res.items():
        tl = (int(data['tl'][0]), int(data['tl'][1]))
        br = (int(data['br'][0]), int(data['br'][1]))
        conf = data['conf']
        cls = data['cls']

        # Drawing bounding box
        # cv2.rectangle(img, tl, br, color, 2)
        # cv2.putText(img, 
        #            "%s: %.2f" % (id2class[cls], conf), 
        #            (tl[0] + 2, tl[1] - 2),
        #            cv2.FONT_HERSHEY_SIMPLEX,
        #            0.8, 
        #            color)

        # Coloring bounding boxes as white
        img[tl[1]:br[1], tl[0]:br[0]] = (255, 255, 255)

    return img
  

inputs = gr.inputs.Image()
outputs = gr.outputs.Image()
inter = gr.Interface(fn=predict, inputs=inputs, outputs=outputs, 
                examples=[
                    ["samples/Parking-in-Japan-05-Private-Lot-Isuzu-Vehicross-640x427.jpg"],
                    ["samples/YT23FXWMOZAG3BVWM2UOWI5SZM.jpg"]
                ])
inter.launch(share=True)
