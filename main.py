from collections import defaultdict
from datetime import datetime
import cv2
import supervision as sv
from ultralytics import YOLO

def run_telemetry_pipeline(video_path: str, output_path: str):
    # Load YOLOv8 model weights (downloads automatically on first run)
    model = YOLO('yolov8n.pt')

    # Initialize video capture from testing folder
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file at {video_path}")
        return

    # Define counting tripwire line coordinates
    START = sv.Point(182, 254)
    END = sv.Point(462, 254)

    # Track trajectories and crossed IDs
    track_history = defaultdict(lambda: [])
    crossed_objects = {}

    # Read video parameters for writing output
    video_info = sv.VideoInfo.from_video_path(video_path)
    
    print("Starting VeloceTrack telemetry processing...")
    
    with sv.VideoSink(output_path, video_info) as sink:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Run YOLOv8 object tracking (cars=2, motorcycles=3, buses=5, trucks=7)
            results = model.track(
                frame, 
                classes=[2, 3, 5, 7], 
                persist=True, 
                tracker="bytetrack.yaml"
            )

            # Check if active tracks exist in frame
            if results[0].boxes is not None and results[0].boxes.id is not None:
                boxes = results[0].boxes.xywh.cpu()
                track_ids = results[0].boxes.id.int().cpu().tolist()

                # Get visual detections frame
                annotated_frame = results[0].plot()

                # Process center coordinates and check line crossings
                for box, track_id in zip(boxes, track_ids):
                    x, y, w, h = box
                    track = track_history[track_id]
                    track.append((float(x), float(y)))
                    
                    if len(track) > 30:
                        track.pop(0)

                    # Trigger line crossing logic
                    if START.x < x < END.x and abs(y - START.y) < 5:
                        if track_id not in crossed_objects:
                            crossed_objects[track_id] = True

                        # Highlight crossing vehicle with a green bounding box
                        cv2.rectangle(
                            annotated_frame, 
                            (int(x - w / 2), int(y - h / 2)), 
                            (int(x + w / 2), int(y + h / 2)), 
                            (0, 255, 0), 
                            2
                        )

                # Render tripwire line on video
                cv2.line(annotated_frame, (START.x, START.y), (END.x, END.y), (0, 255, 0), 2)

                # Render real-time count telemetry HUD
                count_text = f"Vehicles Counted: {len(crossed_objects)}"
                cv2.putText(
                    annotated_frame, 
                    count_text, 
                    (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1, 
                    (0, 255, 0), 
                    2
                )

                # Save processed frame
                sink.write_frame(annotated_frame)

    cap.release()
    cv2.destroyAllWindows()
    print(f"Processing complete! Saved output to {output_path}")

if __name__ == "__main__":
    INPUT_VIDEO = "testing/d.mp4"
    OUTPUT_VIDEO = "testing/output_telemetry.mp4"
    run_telemetry_pipeline(INPUT_VIDEO, OUTPUT_VIDEO)