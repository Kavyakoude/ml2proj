import cv2
import numpy as np
import streamlit as st

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🎯 Virtual Mouse Controller Using Color Detection</h1>", unsafe_allow_html=True)

# Streamlit sliders for yellow color range in HSV
st.sidebar.header("🎨 Yellow Color HSV Range")
yl_h = st.sidebar.slider("Yellow Lower - Hue", 0, 180, 20)
yl_s = st.sidebar.slider("Yellow Lower - Saturation", 0, 255, 100)
yl_v = st.sidebar.slider("Yellow Lower - Value", 0, 255, 100)

yu_h = st.sidebar.slider("Yellow Upper - Hue", 0, 180, 35)
yu_s = st.sidebar.slider("Yellow Upper - Saturation", 0, 255, 255)
yu_v = st.sidebar.slider("Yellow Upper - Value", 0, 255, 255)

lower_yellow = np.array([yl_h, yl_s, yl_v])
upper_yellow = np.array([yu_h, yu_s, yu_v])

# Access webcam using OpenCV
cap = cv2.VideoCapture(0)

frame_placeholder1 = st.empty()
frame_placeholder2 = st.empty()

while True:
    ret, frame = cap.read()
    if not ret:
        st.error("Webcam not accessible")
        break

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Show the frames in Streamlit
    original_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    masked_frame = cv2.cvtColor(cv2.bitwise_and(frame, frame, mask=mask), cv2.COLOR_BGR2RGB)

    frame_placeholder1.image(original_frame, caption="Original Frame", channels="RGB", width=400)
    frame_placeholder2.image(masked_frame, caption="Masked Frame", channels="RGB", width=400)

    if not st.button("Stop"):
        continue
    else:
        break

cap.release()
