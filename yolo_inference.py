from ultralytics import YOLO

model = YOLO('yolov8m')  # Load model

results = model.predict('input_videos/test_video.mp4',save = True)  # Inference on video

print(results[0])  
print("====================================")

for box in results[0].boxes:
    print(box)