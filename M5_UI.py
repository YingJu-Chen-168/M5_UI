import streamlit as st
import sys
import os
import time
import numpy as np
import pyrealsense2 as rs
from ultralytics import YOLO

st.set_page_config(
    page_title="User Interface",
    page_icon="🖋️",
)

st.title("Realsense Live Feed")
st.header('demo', divider= 'rainbow')

W = 640
H = 480

config = rs.config()
config.enable_stream(rs.stream.color, W, H, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, W, H, rs.format.z16, 30)

pipeline = rs.pipeline()
profile = pipeline.start(config)

align_to = rs.stream.color
align = rs.align(align_to)

run = st.checkbox('Run')
FRAME_WINDOW = st.image([])

while run:
    frames = pipeline.wait_for_frames()

    aligned_frames = align.process(frames)
    color_frame = aligned_frames.get_color_frame()
    depth_frame = aligned_frames.get_depth_frame()
    if not color_frame:
        continue

    color_image = np.asanyarray(color_frame.get_data())

    FRAME_WINDOW.image(color_image)
else:
    st.write('Stopped')
