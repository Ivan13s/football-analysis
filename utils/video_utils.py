import cv2 as cv
import numpy as np


# Returns the number of frames in a video
def read_video(video_path):
    cap = cv.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    return frames

def save_video(output_video_frames, output_video_path, fps=24):
    height, width, layers = output_video_frames[0].shape
    # width=output_video_frames[0].shape[1]
    # height=output_video_frames[0].shape[0]
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter(output_video_path, fourcc, fps, (width, height))
    for frame in output_video_frames:
        out.write(frame)
    out.release()
