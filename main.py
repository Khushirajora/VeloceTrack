
from collections import defaultdict
import csv
from datetime import datetime
import cv2
import imageio.v2 as imageio
import supervision as sv
from ultralytics import YOLO



def run_telemetry_pipeline(video_path: str, output_path: str, log_csv_path: str):

    model = YOLO("yolov8n.pt")



    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():

        print(f"Error: Could not open video file at {video_path}")

        return



    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    START = sv.Point(182, 254)

    END = sv.Point(462, 254)



    track_history = defaultdict(list)

    crossed_objects = {}



    # H.264 + yuv420p ensures playback in VS Code, Edge, Chrome, and Windows Media Player

    writer = imageio.get_writer(

        output_path, fps=fps, codec="libx264", pixelformat="yuv420p", quality=8

    )



    with open(log_csv_path, mode="w", newline="") as csv_file:

        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(["Timestamp", "Vehicle_ID", "Vehicle_Type"])



        print("Starting VeloceTrack telemetry processing...")



        while cap.isOpened():

            success, frame = cap.read()

            if not success:

                break



            results = model.track(

                frame,

                classes=[2, 3, 5, 7],

                persist=True,

                tracker="bytetrack.yaml",

                verbose=False

            )



            annotated_frame = frame.copy()



            if results[0].boxes is not None and results[0].boxes.id is not None:

                boxes = results[0].boxes.xywh.cpu()

                track_ids = results[0].boxes.id.int().cpu().tolist()

                class_ids = results[0].boxes.cls.int().cpu().tolist()



                annotated_frame = results[0].plot()



                for box, track_id, class_id in zip(boxes, track_ids, class_ids):

                    x, y, w, h = box

                    track = track_history[track_id]

                    track.append((float(x), float(y)))

                    if len(track) > 30:

                        track.pop(0)



                    # Check tripwire crossing

                    if START.x < x < END.x and abs(y - START.y) < 5:

                        if track_id not in crossed_objects:

                            crossed_objects[track_id] = True

                            vehicle_type = results[0].names[class_id]

                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            csv_writer.writerow([timestamp, track_id, vehicle_type])

                            csv_file.flush()



                        # Highlight crossing vehicle in green

                        cv2.rectangle(

                            annotated_frame,

                            (int(x - w / 2), int(y - h / 2)),

                            (int(x + w / 2), int(y + h / 2)),

                            (0, 255, 0),

                            2

                        )



            # Always draw tripwire, HUD, and write frame even if 0 vehicles are present

            cv2.line(annotated_frame, (START.x, START.y), (END.x, END.y), (0, 255, 0), 2)

            cv2.putText(

                annotated_frame,

                f"Vehicles Counted: {len(crossed_objects)}",

                (10, 30),

                cv2.FONT_HERSHEY_SIMPLEX,

                1,

                (0, 255, 0),

                2

            )



            rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

            writer.append_data(rgb_frame)



    writer.close()

    cap.release()

    print(f"Processing complete! Saved output to {output_path} and {log_csv_path}")



if __name__ == "__main__":

    run_telemetry_pipeline(

        "testing/d.mp4",

        "testing/output_telemetry.mp4",

        "testing/telemetry_log.csv")