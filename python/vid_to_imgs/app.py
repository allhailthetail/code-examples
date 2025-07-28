import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os
import time

# ------------------ Configuration ------------------ #
video_path = "some_recording.mp4"
output_dir = "./slide_screenshots"
ssim_threshold = 0.90        # Lower = more sensitive to changes
min_frame_interval = 30      # Frames to skip between screenshots
frame_skip = 5               # Compare every Nth frame (e.g. every 5th = ~6 FPS)
resize_dim = (320, 240)      # Resize frame to this size for comparison
# --------------------------------------------------- #

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Open video file
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Read first frame
ret, prev_frame = cap.read()
if not ret:
    print("Error: Could not read the first frame.")
    cap.release()
    exit()

# Convert first frame to grayscale and resize
prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_frame_small = cv2.resize(prev_frame_gray, resize_dim)

# Save initial frame
screenshot_count = 0
cv2.imwrite(os.path.join(output_dir, f"slide_{screenshot_count:03d}.png"), prev_frame)
screenshot_count += 1
last_screenshot_frame = 0
frame_count = 0

print("Starting frame analysis...")
start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Skip frames to improve performance
    if frame_count % frame_skip != 0:
        continue

    # Convert current frame
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_small = cv2.resize(frame_gray, resize_dim)

    # Compare SSIM
    similarity, _ = ssim(prev_frame_small, frame_small, full=True)

    if similarity < ssim_threshold and (frame_count - last_screenshot_frame) >= min_frame_interval:
        filename = os.path.join(output_dir, f"slide_{screenshot_count:03d}.png")
        cv2.imwrite(filename, frame)
        print(f"[Frame {frame_count}] Saved {filename} (SSIM={similarity:.4f})")
        screenshot_count += 1
        last_screenshot_frame = frame_count

    prev_frame_small = frame_small

cap.release()
elapsed = time.time() - start_time
print(f"Done. Processed {frame_count} frames in {elapsed:.2f} seconds.")
print(f"Saved {screenshot_count} unique slides to '{output_dir}'.")

