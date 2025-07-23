import streamlit as st
import cv2
import numpy as np

st.set_page_config(layout="wide")
st.title("🎯 Virtual Mouse Detection (Color-Based)")

st.sidebar.header("🎨 HSV Range for Yellow Color")
l_h = st.sidebar.slider("Lower Hue", 0, 180, 20)
l_s = st.sidebar.slider("Lower Saturation", 0, 255, 100)
l_v = st.sidebar.slider("Lower Value", 0, 255, 100)
u_h = st.sidebar.slider("Upper Hue", 0, 180, 40)
u_s = st.sidebar.slider("Upper Saturation", 0, 255, 255)
u_v = st.sidebar.slider("Upper Value", 0, 255, 255)

FRAME_WINDOW = st.image([])

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        st.error("❌ Failed to capture video from webcam.")
        break

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower, upper)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 200 < area < 3000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    FRAME_WINDOW.image(frame, channels="BGR")
