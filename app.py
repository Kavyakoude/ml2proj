# streamlit_app.py

import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(layout="wide")

# Title
st.title("🎯 Virtual Mouse Controller Using Color Detection")

# Sidebar for color calibration
st.sidebar.title("🎨 Color Calibration")

def get_slider(name, default):
    h = st.sidebar.slider(f"{name} - Hue", 0, 180, default[0])
    s = st.sidebar.slider(f"{name} - Saturation", 0, 255, default[1])
    v = st.sidebar.slider(f"{name} - Value", 0, 255, default[2])
    return np.array([h, s, v])

# Color thresholds
yellow_low = get_slider("Yellow Lower", [21, 70, 80])
yellow_high = get_slider("Yellow Upper", [61, 255, 255])

# Webcam capture
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

if ret:
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, yellow_low, yellow_high)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Convert BGR to RGB for display
    stframe1, stframe2 = st.columns(2)
    stframe1.image(frame, caption="Original Frame", channels="BGR")
    stframe2.image(result, caption="Masked Frame", channels="BGR")

    cap.release()
else:
    st.error("Failed to access webcam.")

