import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

ip_address = "http://192.168.0.106:8080/video"
cap = cv2.VideoCapture(ip_address)

if not cap.isOpened():
    print("Error! Could not open the Phone's Camera")
    exit()

brightness_values, times = [], []
starttime = time.time()

while (time.time() - starttime)<15:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    brightness_values.append(brightness)
    times.append(time.time() - starttime)
    cv2.imshow('Feed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

start_idx = np.searchsorted(times, 3)
end_idx = np.searchsorted(times, 13)
segment_times = times[start_idx:end_idx]
segment_brightness = brightness_values[start_idx:end_idx]

if len(segment_brightness) > 0:
    plt.plot(segment_times, segment_brightness)
    plt.xlabel("Time (s)")
    plt.ylabel("Brightness")
    plt.title("Raw PPG (10s Segment)")
    plt.show()
    np.savez("ppg_data.npz", times=segment_times, brightness=segment_brightness)
else:
    print("No valid segment captured.")