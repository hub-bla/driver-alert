import streamlit as st

import cv2
import numpy as np
from utils import preprocess_for_ocr
from scraper import Scraper
from model import FasterRCNN
import torch
import torchvision


scraper = Scraper()
model = FasterRCNN()
model.load("./resources/rcnn_model.pt")


st.title('Driver alert')



img_buffer = st.file_uploader("Choose a file",type=['jpg', 'jpeg', 'png'])
if img_buffer is not None:
    img_raw_bytes = np.asarray(bytearray(img_buffer.read()), dtype=np.uint8)
    img = cv2.imdecode(img_raw_bytes, cv2.IMREAD_COLOR)
    img = cv2.GaussianBlur( img, (3, 3), 0) 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).transpose(2, 0, 1)
    img_tensor = torch.from_numpy(img)
    img = torchvision.transforms.Resize(416, antialias=None)(img_tensor)
    result = model(img)[0]
    boxes = result["boxes"].detach().numpy()
    
    if len(boxes) > 0:
        img = img.detach().numpy().transpose(1, 2, 0)
        st.image(img)
        text, img = preprocess_for_ocr(img, boxes[0])
        if text != '':
            comments = scraper.find_license(text)
            if comments != {}:
                st.write("Found license plate, see comments: ")
                st.write(comments)
            else:
                st.write("License not found")



